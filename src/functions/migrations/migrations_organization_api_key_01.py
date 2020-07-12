from handlers.backend.models import Organizations
from handlers.utils import ApiKeysManager

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get_organizations():
    records, total = Organizations.get_all_organization_records()
    return records


def update_element(records):
    api_key_handler = ApiKeysManager()
    for record in records:
        api_key = api_key_handler.generate_api_key(organization_id=record.to_dict()["id"])
        set_condition = {
            "action": "set",
            "attribute": "api_key",
            "value": api_key
        }
        record.update_record([set_condition])


if __name__ == "__main__":
    organization_records = get_organizations()
    update_element(organization_records)

