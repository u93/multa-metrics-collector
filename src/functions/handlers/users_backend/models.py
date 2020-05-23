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
    MapAttribute,
)

from settings.aws import ORGANIZATIONS_TABLE_NAME, PLANS_TABLE_NAME, ROLES_TABLE_NAME, USERS_TABLE_NAME
from settings.common import MAX_SIZE_PER_PAGE
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.logger


class Plans(Model):
    class Meta:
        table_name = PLANS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    conditions = MapAttribute(null=False)
    price = MapAttribute(null=False)
    last_updated = NumberAttribute(default_for_new=round(time.time()))

    @classmethod
    def create(cls, name: str, conditions: dict, price: dict, id_=None):
        """
        Can be used to create as well to update (if record ID is passed).
        :param name: Plan Name
        :param conditions: Plan conditions that will be shown in the UI
        :param id_: Element ID in DynamoDB
        :return: Class Instance
        """
        cls.validate_table()
        try:
            if id_ is None:
                plan = cls(id=f"{uuid.uuid4()}##{name}", conditions=conditions, price=price, last_updated=round(time.time()))
            else:
                plan = cls(
                    id=id_, conditions=conditions, price=price, last_updated=round(time.time())
                )
            plan.save()
        except Exception:
            logger.error("Error SAVING new PLAN")
            logger.error(traceback.format_exc())
            return False
        else:
            return plan

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING PLAN")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            plans = cls.get_record_by_id(id_=id_)
            for plan in plans:
                plan.delete()
        except Exception:
            logger.error("Error DELETING PLAN by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_id(cls, id_: str):
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
    def get_records(cls, last_evaluated_key=None):
        cls.validate_table()
        try:
            plans = cls.scan(last_evaluated_key=last_evaluated_key, limit=MAX_SIZE_PER_PAGE)
            plans_last_evaluated_key = plans.last_evaluated_key
            plans_total = cls.count()
        except Exception:
            logger.error("Error SCANNING all PLANs")
            logger.error(traceback.format_exc())
            return False
        else:
            return plans, plans_total, plans_last_evaluated_key

    @staticmethod
    def records_to_dict(records):
        try:
            dict_records = [record.to_dict() for record in records]
        except Exception:
            logger.error("Error SCANNING all PLANs")
            logger.error(traceback.format_exc())
            return False
        else:
            return dict_records

    def update_record(self, **kwargs):
        self.validate_table()
        try:
            action_list = list()
            for attr, value in kwargs.items():
                action = getattr(self, attr, None)
                if action is None:
                    continue
                else:
                    action.set(value)
            latest_plan = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING PLAN record")
            logger.error(traceback.format_exc())
            return False
        else:
            return latest_plan

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.id.split("##")[1],
            conditions=self.conditions.as_dict(),
            price=self.price.as_dict(),
            lastUpdated=self.last_updated
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {PLANS_TABLE_NAME} does not exists!")
            raise Exception
