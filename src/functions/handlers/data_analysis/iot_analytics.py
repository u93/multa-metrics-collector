import json
import time
import traceback
import uuid

import boto3

from handlers.common import Sts
from settings.aws import IOT_ANALYTICS_COLD_PATH_KEYS, IOT_ANALYTICS_HOT_PATH_KEYS
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def parse_iot_analytics_message(data: list, analysis: str):
    message_list = list()
    try:
        timestamp = round(time.time())
        for message in data:
            if analysis == "cold_path_metrics":
                payload = json.dumps(get_cold_path_metrics(data=message))
            elif analysis == "connectivity":
                payload = json.dumps(get_connectivity_metrics(data=message, timestamp=timestamp))
            else:
                raise Exception
            message_list.append(dict(messageId=str(uuid.uuid4()), payload=payload))
    except Exception:
        logger.error("Error parsing IoT Analytics message...")
        logger.error(traceback.format_exc())

    logger.info(message_list)
    return message_list


def get_hot_path_metrics(data: dict):
    current_data = data["current"]["state"]["reported"]


def get_connectivity_metrics(data: dict, timestamp):
    response_dict = dict()
    response_dict["serial_number"] = data["thingName"]
    response_dict["thing_id"] = data["thingId"]
    response_dict["thing_type_name"] = data["thingTypeName"]
    response_dict["connection_status"] = data["connectivity"]["connected"]
    response_dict["last_updated_timestamp"] = data["connectivity"]["timestamp"]
    response_dict["timestamp"] = timestamp

    return response_dict


def get_cold_path_metrics(data: dict):
    current_data = data["current"]["state"]["reported"]

    IOT_ANALYTICS_COLD_PATH_KEYS["serial_number"] = data["serial_number"]
    IOT_ANALYTICS_COLD_PATH_KEYS["timestamp"] = round(time.time())
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_total"] = current_data["ram_info"]["raw"]["memory"]["total"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_available"] = current_data["ram_info"]["raw"]["memory"]["available"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_percent"] = current_data["ram_info"]["raw"]["memory"]["percent"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_used"] = current_data["ram_info"]["raw"]["memory"]["used"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_free"] = current_data["ram_info"]["raw"]["memory"]["free"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_shared"] = current_data["ram_info"]["raw"]["memory"]["shared"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_buffers"] = current_data["ram_info"]["raw"]["memory"]["buffers"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_memory_cached"] = current_data["ram_info"]["raw"]["memory"]["cached"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_swap_total"] = current_data["ram_info"]["raw"]["swap"]["total"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_swap_used"] = current_data["ram_info"]["raw"]["swap"]["used"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_swap_free"] = current_data["ram_info"]["raw"]["swap"]["free"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_swap_percent"] = current_data["ram_info"]["raw"]["swap"]["percent"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_insights_current"] = current_data["ram_info"]["insights"]["current"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_insights_total"] = current_data["ram_info"]["insights"]["total"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_insights_percent"] = current_data["ram_info"]["insights"]["percent"]
    IOT_ANALYTICS_COLD_PATH_KEYS["ram_insights_status"] = current_data["ram_info"]["insights"]["status"]

    IOT_ANALYTICS_COLD_PATH_KEYS["cpu_dynamic_insights_percent"] = current_data["cpu_dynamic_info"]["insights"][
        "percent"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["cpu_dynamic_insights_status"] = current_data["cpu_dynamic_info"]["insights"]["high"]

    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_current"] = current_data["disk_dynamic_info"]["current"]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_total"] = current_data["disk_dynamic_info"]["total"]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_percent"] = current_data["disk_dynamic_info"]["percent"]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_insights_status"] = current_data["disk_dynamic_info"]["high"]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_io_read_count"] = current_data["disk_dynamic_info"]["general_io"][
        "read_count"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_io_write_count"] = current_data["disk_dynamic_info"]["general_io"][
        "write_count"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_io_read_bytes"] = current_data["disk_dynamic_info"]["general_io"][
        "read_bytes"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_io_write_bytes"] = current_data["disk_dynamic_info"]["general_io"][
        "write_bytes"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_io_read_time"] = current_data["disk_dynamic_info"]["general_io"][
        "read_time"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["disk_dynamic_io_write_time"] = current_data["disk_dynamic_info"]["general_io"][
        "write_time"
    ]

    IOT_ANALYTICS_COLD_PATH_KEYS["temperature_current"] = current_data["temp_info"]["raw"]["current"]
    IOT_ANALYTICS_COLD_PATH_KEYS["temperature_total"] = current_data["temp_info"]["raw"]["total"]
    IOT_ANALYTICS_COLD_PATH_KEYS["temperature_insights_percent"] = current_data["temp_info"]["insights"]["percent"]
    IOT_ANALYTICS_COLD_PATH_KEYS["temperature_insights_status"] = current_data["temp_info"]["insights"]["high"]

    IOT_ANALYTICS_COLD_PATH_KEYS["boot_time_insights_seconds_since_boot"] = current_data["boot_time_info"]["insights"][
        "seconds_since_boot"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["boot_time_insights_days_since_boot"] = current_data["boot_time_info"]["insights"][
        "days_since_boot"
    ]
    IOT_ANALYTICS_COLD_PATH_KEYS["boot_time_insights_status"] = current_data["boot_time_info"]["insights"]["high"]

    return IOT_ANALYTICS_COLD_PATH_KEYS


class IotAnalyticsHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.iotanalytics_client = boto3.client("iotanalytics")

    def batch_put_message(self, channel_name, messages: list, analysis: str):
        try:
            response = self.iotanalytics_client.batch_put_message(
                channelName=channel_name, messages=parse_iot_analytics_message(data=messages, analysis=analysis)
            )
            return response
        except Exception:
            logger.error("Error putting message...")
            logger.error(traceback.format_exc())
            return False

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
