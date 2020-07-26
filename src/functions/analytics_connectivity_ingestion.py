import time

from handlers.analytics.iot_analytics import IotAnalyticsHandler
from handlers.analytics.iot_things_analytics import IotThingsHandler
from handlers.middleware.api_validation import base_response
from settings.aws import IOT_ANALYTICS_CHANNEL_1
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def lambda_handler(event, context):
    activation_time = round(time.time())
    logger.info(activation_time)
    logger.info(event)

    things_handler = IotThingsHandler()
    results = things_handler.get_things_connectivity()

    analytics_handler = IotAnalyticsHandler()
    put_message_status = analytics_handler.batch_put_message(
        channel_name=IOT_ANALYTICS_CHANNEL_1, messages=results, analysis="connectivity"
    )
    logger.info(put_message_status)

    return base_response(status_code=200)


if __name__ == "__main__":
    event = {
        "version": "0",
        "id": "b73e73b1-7bd9-581f-4729-aab1a3e9f013",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "account": "112646120612",
        "time": "2020-06-11T03:56:00Z",
        "region": "us-east-1",
        "resources": ["arn:aws:events:us-east-1:112646120612:rule/multa_backend_connectivity_collector_dev"],
        "detail": {},
    }
    lambda_handler(event=event, context={})
