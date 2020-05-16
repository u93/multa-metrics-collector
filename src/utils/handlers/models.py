import time
import traceback
import uuid

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UnicodeSetAttribute,
    UTCDateTimeAttribute,
    ListAttribute,
)

from settings.aws import ORGANIZATIONS_TABLE_NAME, PLANS_TABLE_NAME, ROLES_TABLE_NAME, USERS_TABLE_NAME
from settings.common import MAX_SIZE_PER_PAGE
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.logger


class Plans(Model):
    class Meta:
        table_name = PLANS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False, default_for_new=uuid.uuid4())
    name = UnicodeAttribute(null=False)
    conditions = ListAttribute(null=False)
    last_updated = NumberAttribute(default_for_new=round(time.time()))

    @classmethod
    def create(cls, name: str, conditions: list):
        cls.validate_table()
        try:
            if not cls.exists():
                logger.error(f"Table {PLANS_TABLE_NAME} does not exists!")
                raise Exception
            plan = cls(name=name, conditions=conditions, last_updated=round(time.time()))
            plan.save()
        except Exception:
            logger.error("Error SAVING new PLAN")
            logger.error(traceback.format_exc())
            return False
        else:
            return plan

    @classmethod
    def get_record(cls, id_: str):
        cls.validate_table()
        try:
            plan = cls.query(hash_key=id_)
        except Exception:
            logger.error("Error QUERYING individual PLANs")
            logger.error(traceback.format_exc())
            return False
        else:
            return plan

    @classmethod
    def get_records(cls):
        cls.validate_table()
        try:
            plans = cls.scan(consistent_read=True, page_size=MAX_SIZE_PER_PAGE)
            plans_total = cls.count()
        except Exception:
            logger.error("Error SCANNING all PLANs")
            logger.error(traceback.format_exc())
            return False
        else:
            return plans, plans_total

    @classmethod
    def update_record(cls):
        cls.validate_table()
        try:
            plans = cls.update()
            plans_total = cls.count()
        except Exception:
            logger.error("Error SCANNING all PLANs")
            logger.error(traceback.format_exc())
            return False
        else:
            return plans, plans_total

    def to_dict(self):
        return dict(id=self.id, name=self.name, conditions=self.conditions, lastUpdated=self.last_updated)

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {PLANS_TABLE_NAME} does not exists!")
            raise Exception
