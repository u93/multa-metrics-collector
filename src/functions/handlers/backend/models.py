import secrets
import time
import traceback
import uuid

from pynamodb.attributes import (
    UnicodeAttribute,
    BooleanAttribute,
    NumberAttribute,
    # UnicodeSetAttribute,
    # UTCDateTimeAttribute,
    ListAttribute,
    MapAttribute,
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model

from handlers.utils import ApiKeysManager
from settings.aws import (
    ORGANIZATIONS_TABLE_NAME,
    PLANS_TABLE_NAME,
    ROLES_TABLE_NAME,
    SERVICE_TOKENS_TABLE_NAME,
    USERS_TABLE_NAME,
)
from settings.common import MAX_SIZE_PER_PAGE, SERVICE_TOKEN_BYTES
from settings.logs import Logger
from settings.models import COMPONENT_IDS, GLOBAL_INDEXES

logs_handler = Logger()
logger = logs_handler.logger


class ApiKeysIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = GLOBAL_INDEXES["API_KEYS_INDEX"]
        read_capacity_units = 2
        write_capacity_units = 1
        projection = AllProjection()

    api_key = UnicodeAttribute(hash_key=True, null=False)


class ElementIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = GLOBAL_INDEXES["ELEMENT_ID_INDEX"]
        read_capacity_units = 2
        write_capacity_units = 1
        projection = AllProjection()

    element_id = UnicodeAttribute(hash_key=True, null=False)


class Organizations(Model):
    class Meta:
        table_name = ORGANIZATIONS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    setting_id = UnicodeAttribute(range_key=True, null=False)
    element_id_index = ElementIdIndex()
    element_id = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    plan = UnicodeAttribute(null=False)
    owner = UnicodeAttribute(null=False)
    api_key_index = ApiKeysIndex()
    api_key = UnicodeAttribute(null=False)
    is_valid = BooleanAttribute(null=False, default_for_new=True)
    creation_time = NumberAttribute(null=False, default_for_new=round(time.time()))
    billing_time = NumberAttribute(null=True, default_for_new=None)
    last_updated = NumberAttribute(null=False, default_for_new=round(time.time()))

    @classmethod
    def create(cls, name: str, plan: str, owner: dict, organization_id=None, billing_time=None, is_valid=True):
        """
        Can be used to create as well to update (if record ID is passed).
        :param name: Organization Name
        :param plan: Plan ID in DynamoDB.
        :param owner: User ID in DynamoDB.
        :param organization_id: Element ID in DynamoDB.
        :param billing_time:
        :param is_valid:
        :return: Class Instance
        """
        cls.validate_table()
        api_key_manager = ApiKeysManager()
        try:
            if organization_id is None:
                organization_id = str(uuid.uuid4())
                organization = cls(
                    id=organization_id,
                    setting_id=COMPONENT_IDS["ORGANIZATION"],
                    element_id=organization_id,
                    name=name,
                    plan=plan,
                    owner=owner,
                    is_valid=is_valid,
                    api_key=api_key_manager.generate_api_key(organization_id=organization_id),
                    creation_time=round(time.time()),
                    last_updated=round(time.time()),
                    billing_time=billing_time,
                )
            else:
                organization = cls(
                    id=organization_id,
                    setting_id=COMPONENT_IDS["ORGANIZATION"],
                    element_id=str(uuid.uuid4()),
                    plan=plan,
                    owner=owner,
                    is_valid=is_valid,
                    api_key=api_key_manager.generate_api_key(organization_id=organization_id),
                    creation_time=round(time.time()),
                    last_updated=round(time.time()),
                    billing_time=billing_time,
                )
            organization.save()

        except Exception:
            logger.error("Error SAVING new ORGANIZATION")
            logger.error(traceback.format_exc())
            return False
        else:
            return organization

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING ORGANIZATION")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            organization = cls.get_record_by_id(id_=id_)
            organization.delete()
        except Exception:
            logger.error("Error DELETING ORGANIZATION by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_api_key(cls, id_):
        cls.validate_table()
        try:
            records = cls.api_key_index.query(hash_key=id_, limit=1)
            for record in records:
                return record

            logger.info(f"No API KEY found by id - {id_}")
            return False

        except Exception:
            logger.error("Error QUERYING individual API KEYS")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def get_record_by_element_id(cls, id_):
        cls.validate_table()
        try:
            records = cls.element_id_index.query(hash_key=id_, limit=1)
            for record in records:
                return record

            logger.info(f"No API KEY found by id - {id_}")
            return False

        except Exception:
            logger.error("Error QUERYING individual API KEYS")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def get_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            organization_records = cls.query(
                hash_key=id_, filter_condition=Organizations.element_id.contains(id_), limit=1
            )
            for organization in organization_records:
                return organization

            logger.info(f"No ORGANZATION found by id {id_}")
            return False

        except Exception:
            logger.error("Error QUERYING individual ORGANIZATIONS")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def get_records(cls, organization_id: str, last_evaluated_key=None):
        cls.validate_table()
        records = list()
        try:
            # users = cls.scan(last_evaluated_key=last_evaluated_key, limit=MAX_SIZE_PER_PAGE)
            kwargs = dict(
                hash_key=organization_id,
                range_key_condition=Users.setting_id.startswith(COMPONENT_IDS["ORGANIZATION"]),
                limit=MAX_SIZE_PER_PAGE,
            )
            while True:
                user_records = cls.query(**kwargs)
                records.extend(user_records)
                if user_records.last_evaluated_key is not None:
                    kwargs["last_evaluated_key"] = last_evaluated_key
                else:
                    break

            total_elements = cls.count()
        except Exception:
            logger.error("Error GETTING all USERs")
            logger.error(traceback.format_exc())
            logger.error(records)
            return False
        else:
            return records, total_elements

    @classmethod
    def get_all_organization_records(cls, last_evaluated_key=None):
        cls.validate_table()
        records = list()
        try:
            kwargs = dict(
                limit=MAX_SIZE_PER_PAGE,
                filter_condition=Organizations.setting_id.startswith(COMPONENT_IDS["ORGANIZATION"]),
            )
            while True:
                organization_records = cls.scan(**kwargs)
                records.extend(organization_records)
                if organization_records.last_evaluated_key is not None:
                    kwargs["last_evaluated_key"] = last_evaluated_key
                else:
                    break

            total_elements = cls.count()
        except Exception:
            logger.error("Error SCANNING all ORGANIZATIONs")
            logger.error(traceback.format_exc())
            return False
        else:
            return records, total_elements

    @staticmethod
    def records_to_dict(records):
        try:
            dict_records = [record.to_dict() for record in records]
        except Exception:
            logger.error("Error SCANNING all ORGANIZATIONS")
            logger.error(traceback.format_exc())
            return False
        else:
            return dict_records

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING ORGANIZATION record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            settingId=self.setting_id,
            elementId=self.element_id,
            plan=self.plan,
            owner=self.owner,
            apiKey=self.api_key,
            creationTime=self.creation_time,
            lastUpdated=self.last_updated,
            billingTime=self.billing_time,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {ORGANIZATIONS_TABLE_NAME} does not exists!")
            raise Exception


class Devices(Model):
    class Meta:
        table_name = ORGANIZATIONS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    setting_id = UnicodeAttribute(range_key=True, null=False)
    element_id = UnicodeAttribute(null=False)
    data = MapAttribute(default_for_new=dict())
    is_valid = BooleanAttribute(null=False, default_for_new=True)
    creation_time = NumberAttribute(null=False, default_for_new=round(time.time()))

    @classmethod
    def create(cls, device_name: str, organization_id: str, is_valid=True):
        """
        Can be used to create as well to update (if record ID is passed).
        :param device_name: AWS IoT Device name.
        :param organization_id: Element ID in DynamoDB.
        :param is_valid: If user account is Valid or not.
        :return: Class Instance
        """
        cls.validate_table()
        try:
            user = cls(
                id=organization_id,
                setting_id=f"{COMPONENT_IDS['DEVICE']}##{device_name}",
                element_id=f"{device_name}",
                is_valid=is_valid,
                creation_time=round(time.time()),
            )
            user.save()
        except Exception:
            logger.error("Error SAVING new DEVICE")
            logger.error(traceback.format_exc())
            return False
        else:
            return user

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING DEVICE")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, organization_id: str, device_name: str):
        cls.validate_table()
        try:
            user = cls.get_record_by_id(organization_id=organization_id, device_name=device_name)
            user.delete()
        except Exception:
            logger.error("Error DELETING DEVICE by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_id(cls, organization_id: str, device_name: str):
        cls.validate_table()
        try:
            records = cls.query(
                hash_key=organization_id, range_key_condition=Devices.element_id.contains(device_name), limit=1
            )
            for record in records:
                return record
        except Exception:
            logger.error("Error QUERYING individual DEVICES")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def get_records(cls, organization_id: str, last_evaluated_key=None):
        cls.validate_table()
        result_records = list()
        try:
            kwargs = dict(
                hash_key=organization_id,
                range_key_condition=Users.setting_id.startswith(COMPONENT_IDS["DEVICE"]),
                limit=MAX_SIZE_PER_PAGE,
            )
            while True:
                records = cls.query(**kwargs)
                result_records.extend(records)
                if records.last_evaluated_key is not None:
                    kwargs["last_evaluated_key"] = last_evaluated_key
                else:
                    break

            total_elements = cls.count()
        except Exception:
            logger.error("Error GETTING all DEVICEs")
            logger.error(traceback.format_exc())
            logger.error(result_records)
            return False
        else:
            return result_records, total_elements

    @staticmethod
    def records_to_dict(records):
        try:
            dict_records = [record.to_dict() for record in records]
        except Exception:
            logger.error("Error PARSING TO DICT all DEVICEs")
            logger.error(traceback.format_exc())
            return False
        else:
            return dict_records

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING USER record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.element_id,
            organizationId=self.id,
            settingId=self.setting_id,
            data=self.data.as_dict(),
            isValid=self.is_valid,
            creationTime=self.creation_time,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {ORGANIZATIONS_TABLE_NAME} does not exists!")
            raise Exception


class Users(Model):
    class Meta:
        table_name = ORGANIZATIONS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    setting_id = UnicodeAttribute(range_key=True, null=False)
    element_id = UnicodeAttribute(null=False)
    role = UnicodeAttribute(null=False)
    is_valid = BooleanAttribute(null=False, default_for_new=True)
    creation_time = NumberAttribute(null=False, default_for_new=round(time.time()))
    last_updated = NumberAttribute(null=False, default_for_new=round(time.time()))

    @classmethod
    def create(cls, user_id: str, role: str, organization_id: str, is_valid=True):
        """
        Can be used to create as well to update (if record ID is passed).
        :param user_id: Cognito User ID.
        :param role: Plan ID in DynamoDB.
        :param organization_id: Element ID in DynamoDB.
        :param is_valid: If user account is Valid or not.
        :return: Class Instance
        """
        cls.validate_table()
        try:
            user = cls(
                id=organization_id,
                setting_id=f"{COMPONENT_IDS['USER']}##{user_id}",
                element_id=user_id,
                role=role,
                is_valid=is_valid,
                creation_time=round(time.time()),
                last_updated=round(time.time()),
            )
            user.save()
        except Exception:
            logger.error("Error SAVING new USER")
            logger.error(traceback.format_exc())
            return False
        else:
            return user

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING USER")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, organization_id: str, user_id: str):
        cls.validate_table()
        try:
            user = cls.get_record_by_id(organization_id=organization_id, user_id=user_id)
            user.delete()
        except Exception:
            logger.error("Error DELETING USER by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_id(cls, organization_id: str, user_id: str):
        cls.validate_table()
        try:
            user_records = cls.query(
                hash_key=organization_id, range_key_condition=Users.element_id.contains(user_id), limit=1
            )
            for user in user_records:
                return user
        except Exception:
            logger.error("Error QUERYING individual USER")
            logger.error(traceback.format_exc())
            return False

    @classmethod
    def get_records(cls, organization_id: str, last_evaluated_key=None):
        cls.validate_table()
        records = list()
        try:
            # users = cls.scan(last_evaluated_key=last_evaluated_key, limit=MAX_SIZE_PER_PAGE)
            kwargs = dict(
                hash_key=organization_id,
                range_key_condition=Users.setting_id.startswith(COMPONENT_IDS["USER"]),
                limit=MAX_SIZE_PER_PAGE,
            )
            while True:
                user_records = cls.query(**kwargs)
                records.extend(user_records)
                if user_records.last_evaluated_key is not None:
                    kwargs["last_evaluated_key"] = last_evaluated_key
                else:
                    break

            total_elements = cls.count()
        except Exception:
            logger.error("Error GETTING all USERs")
            logger.error(traceback.format_exc())
            logger.error(records)
            return False
        else:
            return records, total_elements

    @staticmethod
    def records_to_dict(records):
        try:
            dict_records = [record.to_dict() for record in records]
        except Exception:
            logger.error("Error SCANNING all USERs")
            logger.error(traceback.format_exc())
            return False
        else:
            return dict_records

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING USER record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.element_id,
            organizationId=self.id,
            settingId=self.setting_id,
            role=self.role,
            creationTime=self.creation_time,
            lastUpdated=self.last_updated,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {ORGANIZATIONS_TABLE_NAME} does not exists!")
            raise Exception


class UserOrganizationRelation(Model):
    class Meta:
        table_name = USERS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    organization_id = UnicodeAttribute(null=False)
    creation_time = NumberAttribute(null=False, default_for_new=round(time.time()))
    last_updated = NumberAttribute(null=False, default_for_new=round(time.time()))

    @classmethod
    def create(cls, user_id: str, organization_id: str):
        """
        Can be used to create as well to update (if record ID is passed).
        :param user_id: User ID in Cognito.
        :param organization_id: Organization ID in DynamoDB.
        :return: Class Instance
        """
        cls.validate_table()
        try:
            user = cls(
                id=user_id,
                organization_id=organization_id,
                creation_time=round(time.time()),
                last_updated=round(time.time()),
            )
            user.save()
        except Exception:
            logger.error("Error SAVING new USER ORGANIZATION RELATION")
            logger.error(traceback.format_exc())
            return False
        else:
            return user

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING USER ORGANIZATION RELATION")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            user = cls.get_record_by_id(id_=id_)
            user.delete()
        except Exception:
            logger.error("Error DELETING USER ORGANIZATION RELATION by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            user_records = cls.query(hash_key=id_, limit=1)
            for user in user_records:
                return user
        except Exception:
            logger.error("Error QUERYING individual USER ORGANIZATION RELATION")
            logger.error(traceback.format_exc())

        return False

    @classmethod
    def get_records(cls, last_evaluated_key=None):
        cls.validate_table()
        try:
            users = cls.scan(last_evaluated_key=last_evaluated_key, limit=MAX_SIZE_PER_PAGE)
            users_last_evaluated_key = users.last_evaluated_key
            users_total = cls.count()
        except Exception:
            logger.error("Error SCANNING all USER ORGANIZATION RELATIONs")
            logger.error(traceback.format_exc())
            return False
        else:
            return users, users_last_evaluated_key, users_total

    @staticmethod
    def records_to_dict(records):
        try:
            dict_records = [record.to_dict() for record in records]
        except Exception:
            logger.error("Error SCANNING all USER ORGANIZATION RELATIONs")
            logger.error(traceback.format_exc())
            return False
        else:
            return dict_records

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING USER/ORGANIZATION record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.id,
            organizationId=self.organization_id,
            creationTime=self.creation_time,
            lastUpdated=self.last_updated,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {ORGANIZATIONS_TABLE_NAME} does not exists!")
            raise Exception


class ServiceTokens(Model):
    class Meta:
        table_name = SERVICE_TOKENS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    value = UnicodeAttribute(null=False)
    is_valid = BooleanAttribute(null=False, default_for_new=True)
    created_time = NumberAttribute(default_for_new=round(time.time()))
    last_updated = NumberAttribute(default_for_new=round(time.time()))

    @classmethod
    def create(cls, id_=None, value=None, is_valid=None, created_time=None):
        """
        Can be used to create a Service Token.
        :return: Class Instance
        """
        cls.validate_table()
        try:
            if id_ is None:
                token = cls(
                    id=f"{uuid.uuid4()}",
                    value=secrets.token_hex(SERVICE_TOKEN_BYTES),
                    # TODO: ADD ROLE
                    is_valid=True,
                    created_time=round(time.time()),
                    last_updated=round(time.time()),
                )
            else:
                token = cls(
                    id=id_,
                    value=value,
                    # TODO: ADD ROLE
                    is_valid=is_valid,
                    created_time=created_time,
                    last_updated=round(time.time()),
                )
            token.save()
        except Exception:
            logger.error("Error SAVING new SERVICE TOKEN")
            logger.error(traceback.format_exc())
            return False
        else:
            return token

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING SERVICE TOKEN")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            tokens = cls.get_record_by_id(id_=id_)
            for token in tokens:
                token.delete()
        except Exception:
            logger.error("Error DELETING SERVICE TOKEN by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            token = cls.query(hash_key=id_)
        except Exception:
            logger.error("Error QUERYING individual SERVICE TOKEN")
            logger.error(traceback.format_exc())
            return False
        else:
            return token

    @classmethod
    def get_records(cls, last_evaluated_key=None):
        cls.validate_table()
        try:
            tokens = cls.scan(last_evaluated_key=last_evaluated_key, limit=MAX_SIZE_PER_PAGE)
            tokens_last_evaluated_key = tokens.last_evaluated_key
            tokens_total = cls.count()
        except Exception:
            logger.error("Error SCANNING all TOKENS")
            logger.error(traceback.format_exc())
            return False
        else:
            return tokens, tokens_total, tokens_last_evaluated_key

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

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING SERVICETOKEN record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.id,
            value=self.value,
            isValid=self.is_valid,
            createdTime=self.created_time,
            lastUpdated=self.last_updated,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {SERVICE_TOKENS_TABLE_NAME} does not exists!")
            raise Exception


class InternalRoleGroup(MapAttribute):
    rest_api_id = UnicodeAttribute()
    stage = UnicodeAttribute()
    method = UnicodeAttribute()
    resources = ListAttribute()


class Roles(Model):
    class Meta:
        table_name = ROLES_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    index = NumberAttribute(null=False)
    logic_groups = ListAttribute(null=False, of=InternalRoleGroup)
    last_updated = NumberAttribute(default_for_new=round(time.time()))

    @classmethod
    def create(cls, name: str, index: int, logic_groups: list, id_=None):
        """
        Can be used to create as well to update (if record ID is passed).
        :param name: Plan Name
        :param index: Index to be used by the FE.
        :param logic_groups: Plan conditions that will be shown in the UI.
        :param id_: Element ID in DynamoDB.
        :return: Class Instance.
        """
        cls.validate_table()
        try:
            if id_ is None:
                role = cls(
                    id=f"{uuid.uuid4()}##{name}",
                    index=index,
                    logic_groups=logic_groups,
                    last_updated=round(time.time()),
                )
            else:
                role = cls(id=id_, index=index, logic_groups=logic_groups, last_updated=round(time.time()))
            role.save()
        except Exception:
            logger.error("Error SAVING new ROLE")
            logger.error(traceback.format_exc())
            return False
        else:
            return role

    def delete_record(self):
        try:
            self.delete()
        except Exception:
            logger.error("Error DELETING ROLE")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def delete_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            role = cls.get_record_by_id(id_=id_)
            role.delete()
        except Exception:
            logger.error("Error DELETING ROLE by id")
            logger.error(traceback.format_exc())
            return False
        else:
            return True

    @classmethod
    def get_record_by_id(cls, id_: str):
        cls.validate_table()
        try:
            roles = cls.query(hash_key=id_, limit=1)
            for role in roles:
                return role
        except Exception:
            logger.error("Error QUERYING individual ROLE")
            logger.error(traceback.format_exc())

        return False

    @classmethod
    def get_records(cls, last_evaluated_key=None):
        cls.validate_table()
        try:
            roles = cls.scan(last_evaluated_key=last_evaluated_key, limit=MAX_SIZE_PER_PAGE)
            roles_last_evaluated_key = roles.last_evaluated_key
            roles_total = cls.count()
        except Exception:
            logger.error("Error SCANNING all ROLEs")
            logger.error(traceback.format_exc())
            return False
        else:
            return roles, roles_total, roles_last_evaluated_key

    @staticmethod
    def records_to_dict(records):
        try:
            dict_records = [record.to_dict() for record in records]
        except Exception:
            logger.error("Error SCANNING all ROLEs")
            logger.error(traceback.format_exc())
            return False
        else:
            return dict_records

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING ROLE record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.id.split("##")[1].capitalize(),
            index=self.index,
            logic_groups=[logic_group.as_dict() for logic_group in self.logic_groups],
            lastUpdated=self.last_updated,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {PLANS_TABLE_NAME} does not exists!")
            raise Exception


class Plans(Model):
    class Meta:
        table_name = PLANS_TABLE_NAME

    id = UnicodeAttribute(hash_key=True, null=False)
    index = NumberAttribute(null=False)
    conditions = MapAttribute(null=False)
    price = MapAttribute(null=False)
    last_updated = NumberAttribute(default_for_new=round(time.time()))

    @classmethod
    def create(cls, name: str, index: int, conditions: dict, price: dict, id_=None):
        """
        Can be used to create as well to update (if record ID is passed).
        :param name: Plan Name
        :param index: Index in table for FE to use.
        :param conditions: Plan conditions that will be shown in the UI
        :param id_: Element ID in DynamoDB
        :return: Class Instance
        """
        cls.validate_table()
        try:
            if id_ is None:
                plan = cls(
                    id=f"{uuid.uuid4()}##{name}",
                    index=index,
                    conditions=conditions,
                    price=price,
                    last_updated=round(time.time()),
                )
            else:
                plan = cls(id=id_, index=index, conditions=conditions, price=price, last_updated=round(time.time()))
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
            plan = cls.get_record_by_id(id_=id_)
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
            plans = cls.query(hash_key=id_)
            for plan in plans:
                return plan
        except Exception:
            logger.error("Error QUERYING individual PLANs")
            logger.error(traceback.format_exc())

        return False

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

    def update_record(self, values: list):
        self.validate_table()
        try:
            action_list = list()
            for value in values:
                attribute = self.get_attributes().get(value["attribute"])
                if attribute is None:
                    continue

                action = getattr(attribute, value["action"])
                attribute_value = value["value"]
                action_list.append(action(attribute_value))

            record = self.update(actions=action_list)
        except Exception:
            logger.error("Error UPDATING PLAN record")
            logger.error(traceback.format_exc())
            return False
        else:
            return record

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.id.split("##")[1],
            index=self.index,
            conditions=self.conditions.as_dict(),
            price=self.price.as_dict(),
            lastUpdated=self.last_updated,
        )

    @classmethod
    def validate_table(cls):
        if not cls.exists():
            logger.error(f"Table {PLANS_TABLE_NAME} does not exists!")
            raise Exception
