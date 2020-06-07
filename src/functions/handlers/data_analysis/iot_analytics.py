import traceback

import boto3

from handlers.common import Sts
from settings.aws import IOT_ANALYTICS_COLD_PATH_KEYS, IOT_ANALYTICS_HOT_PATH_KEYS
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def parse_iot_analytics_message(data):
    pass


def get_cold_path_metrics(data: dict):
    pass


def get_hor_path_metrics(data: dict):
    pass


class IotAnalyticsHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.iotanalytics_client = boto3.client("iotanalytics")

    def batch_put_message(self):
        pass

    def create_dataset(self):
        pass

    def get_dataset_content(self):
        pass

    def list_datasets(self):
        pass

    def list_datasets_contents(self):
        pass

    def refresh_dataset(self):
        pass