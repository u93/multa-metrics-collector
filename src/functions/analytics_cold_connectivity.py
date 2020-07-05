import json
import os
import time
import uuid

from handlers.utils import base_response
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get():
    pass


def post():
    pass


def put():
    pass


def patch():
    pass


def delete():
    pass


def lambda_handler(event, context):
    activation_time = round(time.time())
    logger.info(activation_time)
    logger.info(os.environ)
    logger.info(event)

    return {"time": activation_time, "status": 200, "metric": "connectivity", "id": str(uuid.uuid4())}


if __name__ == "__main__":
    event = {
        "analysis": "average",
        "parameters": {
            "metric_value": "123",
            "metric_range": "123",
            "start_time": "123",
            "end_time": "123",
            "start_date": "123",
            "end_date": "123",
            "start_timestamp": 123,
            "end_timestamp": 123,
            "agents": ["123", "123"],
            "metadata": {"key": "value"},
        },
    }
    lambda_handler(event=event, context={})
