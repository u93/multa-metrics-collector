from datetime import datetime
import json
import time
import traceback
import uuid

import boto3

from handlers.common import Sts
from settings.aws import (
    IOT_ANALYTICS_COLD_PATH_KEYS,
    IOT_ANALYTICS_HOT_PATH_KEYS,
    IOT_ANALYTICS_DATASTORE_0,
    IOT_ANALYTICS_DATASTORE_1,
)
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


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

    @staticmethod
    def parse_analysis(analysis_type="SYNC"):
        if analysis_type == "SYNC":
            return IOT_ANALYTICS_DATASTORE_0
        elif analysis_type == "ASYNC":
            return IOT_ANALYTICS_DATASTORE_1
        else:
            return False

    @staticmethod
    def get_query(params: str, dstore: str, order: str, limit, stime_etime):
        try:
            parameters = f"SELECT {params}"
            datastore = f"FROM {dstore}"
            sql_query = f"{parameters} {datastore}"

            if stime_etime is not None:
                stime_etime = stime_etime.split(",")
                where_query_format = f"WHERE timestamp >= {stime_etime[0]} AND timestamp <= {stime_etime[1]}"
                sql_query = f"{sql_query} {where_query_format}"

            order = f"ORDER BY timestamp {order}"
            sql_query = f"{sql_query} {order}"

            if limit is not None:
                limit = f"LIMIT {limit}"
                sql_query = f"{sql_query} {limit}"

            return sql_query
        except Exception:
            logger.error("Error creating SQL query")
            logger.error(traceback.format_exc())
            return False

    @staticmethod
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

        # logger.info(message_list)
        return message_list

    def batch_put_message(self, channel_name, messages: list, analysis: str):
        try:
            response = self.iotanalytics_client.batch_put_message(
                channelName=channel_name, messages=self.parse_iot_analytics_message(data=messages, analysis=analysis)
            )
            return response
        except Exception:
            logger.error("Error putting message...")
            logger.error(traceback.format_exc())
            return False

    def create_dataset(
            self,
            dset: str,
            org_id: str,
            params: str,
            analysis: str,
            order="DESC",
            limit=None,
            stime_etime=None,
    ):
        """
        Creates Dataset with SQL Action.
        :param dset: Dataset Name (obtained from FE).
        :param org_id: Organization ID (obtained from FE or from Internal Query).
        :param params: Desired parameters (obtained from FE - At least should receive '*').
        :param analysis: Analysis Type (obtained from FE - Should be 'SYNC' or 'ASYNC').
        :param order: Desired order for Data Analysis. Defaults to DESC (obtained from FE - Should be 'DESC' or 'ASC').
        :param limit: Desired limit of data. Defaults to None (obtained from FE - Should be a number).
        :param stime_etime: Desired start time and end time for Query. Defaults to None (obtained from FE - Should be '#,#').
        :return: Dataset Name or False.
        """
        try:
            dataset_name = f"{org_id.replace('-', '_')}_{dset}"
            datastore = self.parse_analysis(analysis_type=analysis)
            if datastore is False:
                return False

            sql_query = self.get_query(params, datastore, order, limit, stime_etime)
            if sql_query is False:
                return False

            response = self.iotanalytics_client.create_dataset(
                datasetName=dataset_name,
                actions=[{"actionName": dataset_name, "queryAction": {"sqlQuery": sql_query},},],
                tags=[{"key": "organization", "value": org_id,},]
            )
            return response["datasetName"]
        except Exception:
            logger.error("Error CREATING dataset...")
            logger.error(traceback.format_exc())
            return False

    def get_dataset_content(self, dataset_name: str, version_id="$LATEST"):
        """
        Returns HTTPS URL for Dataset CSV Data if request succeeds or False if fails. Waits until Dataset is refreshed.
        :param dataset_name: Dataset name obtained from a previous request or environment variable.
        :param version_id: Defaults to latest but accepts custom version ID obtained from a previous request.
        :return: Dataset URL or False.
        """
        try:
            while True:
                response = self.iotanalytics_client.get_dataset_content(
                    datasetName=dataset_name,
                    versionId=version_id
                )
                if response["status"]["state"] == "CREATING":
                    logger.info("CREATING")
                    time.sleep(1)
                elif response["status"]["state"] == "SUCCEEDED":
                    logger.info("SUCCEEDED")
                    break
                elif response["status"]["state"] == "FAILED":
                    logger.error("FAILED")
                    return False
                else:
                    logger.error("UNEXPECTED ERROR!!!")
                    return False
            return response["entries"][0]["dataURI"]
        except Exception:
            logger.error("Error when GETTING dataset content...")
            logger.error(traceback.format_exc())
            return False

    def list_datasets(self):
        """
        Returns a list of AWS Account Datasets summaries. Contains name, status, last update, actions, etc.
        :return: List of Datasets or False.
        """
        try:
            response_list = list()
            kwargs = {
                "maxResults": 200,
            }
            while True:
                response = self.iotanalytics_client.list_datasets(**kwargs)
                response_list.extend(response["datasetSummaries"])
                if "nextToken" in response:
                    kwargs["nextToken"] = response["nextToken"]
                else:
                    break
            return response_list

        except Exception:
            logger.error("Error when LISTING datasets...")
            logger.error(traceback.format_exc())
            return False

    def list_datasets_contents(self, dataset_name: str, start_timestamp=None):
        """
        Returns a list of AWS Account Datasets Contents summaries. Contains version, status, create time, completion time, etc.
        :return: List of Datasets Contents or False.
        """
        try:
            response_list = list()
            kwargs = {
                "datasetName": dataset_name,
                "maxResults": 200,
            }
            if isinstance(start_timestamp, int):
                kwargs["scheduledOnOrAfter"] = datetime.fromtimestamp(start_timestamp)

            while True:
                response = self.iotanalytics_client.list_dataset_contents(**kwargs)
                response_list.extend(response["datasetContentSummaries"])
                if "nextToken" in response:
                    kwargs["nextToken"] = response["nextToken"]
                else:
                    break
            return response_list

        except Exception:
            logger.error("Error when LISTING datasets contents...")
            logger.error(traceback.format_exc())
            return False

    def refresh_dataset(self, dataset_name: str):
        """
        Refreshes or creates if the dataset content has not been created.
        Async request, will not wait until content is available.
        :param dataset_name: Name of the desired Dataset to refresh/create content.
        :return: Version ID of Dataset content or False.
        """
        try:
            response = self.iotanalytics_client.create_dataset_content(
                datasetName=dataset_name
            )
            return response["versionId"]
        except Exception:
            logger.error("Error when REFRESING dataset content...")
            logger.error(traceback.format_exc())
            return False


if __name__ == "__main__":
    handler = IotAnalyticsHandler()

    # datasets_list = handler.list_datasets()
    # logger.info(datasets_list)
    #
    # dset_name = "test_create_func"
    # datasets_list = handler.list_datasets_contents(dataset_name=dset_name)
    # logger.info(datasets_list)

    # dset_name = "test_create_func"
    # organization_id = "test-org-id2-2"
    # params = "*"
    # datastore_name = "multa_backend_analytics_connectivity_pipeline_datastore_dev"
    # limit = 100
    # stime_etime = "1592160000,1592163120"
    # dataset = handler.create_dataset(
    #     dset=dset_name, org_id=organization_id, params=params, dstore=datastore_name, limit=limit, stime_etime=stime_etime
    # )
    # logger.info(dataset)

    # dset_final_name = "test_create_func"
    # dataset_content_refresh_action = handler.refresh_dataset(dataset_name=dset_final_name)
    # logger.info(dataset_content_refresh_action)
    #
    # dset_final_name = "test_create_func"
    # # version_id = "c4bc2695-4748-4581-a6c3-8ff0c92c69aa"
    # dataset_content_get_action = handler.get_dataset_content(dataset_name=dset_final_name)
    # logger.info(dataset_content_get_action)



