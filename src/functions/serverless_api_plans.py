import traceback

from handlers.backend.models import Plans
from handlers.utils import base_response

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get(event, **kwargs):
    try:
        record_plans, total_records, roles_last_evaluated_key = Plans.get_records()
        current_plans = Plans.records_to_dict(record_plans)
    except Exception:
        logger.error("Error GETTING current plans")
        logger.error(traceback.format_exc())
        return False

    return current_plans


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
        current_plans = get(event=event)
        if current_plans is False:
            return base_response(status_code=500, dict_body=dict(results=False, error="Error getting account plans..."))
        logger.info(dict(results=current_plans))
        return base_response(status_code=200, dict_body=dict(results=dict(data=current_plans)))

    else:
        return base_response(status_code=400, dict_body=dict(results=False, error="Unhandled method..."))


if __name__ == "__main__":
    event = {"httpMethod": "GET"}
    lambda_handler(event=event, context={})
