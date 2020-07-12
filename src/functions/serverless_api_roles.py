import traceback

from handlers.users_backend.models import Roles
from handlers.utils import base_response

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get(event, **kwargs):
    try:
        record_roles, total_records, roles_last_evaluated_key = Roles.get_records()
        current_roles = Roles.records_to_dict(record_roles)
    except Exception:
        logger.error("Error GETTING current roles")
        logger.error(traceback.format_exc())
        return False

    return current_roles


def post():
    pass


def put():
    pass


def patch():
    pass


def delete():
    pass


def lambda_handler(event, context):
    logger.info(event)

    http_method = event["httpMethod"]
    if http_method == "GET":
        current_roles = get(event=event)
        if current_roles is False:
            return base_response(status_code=500, dict_body=dict(results=False, error="Error getting account roles..."))
        logger.info(dict(results=current_roles))
        return base_response(status_code=200, dict_body=dict(results=dict(data=current_roles)))

    else:
        return base_response(status_code=400, dict_body=dict(results=False, error="Unhandled method..."))


event = {"httpMethod": "GET"}
lambda_handler(event=event, context={})
