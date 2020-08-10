import json
import traceback

import boto3

from handlers.common import Sts
from settings.aws import IOT_ANALYTICS_HOT_PATH_SEARCH_MAPPING
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def filter_thing_index_search(results: list, parameters: list):
    updated_results = list()
    for result in results:
        for parameter in parameters:
            try:
                del result[parameter]
            except Exception:
                logger.error(f"Error deleting parameter {parameter}...")
        updated_results.append(result)

    return updated_results


class IotThingsHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.iotthings_client = boto3.client("iot")
        self.iotthings_data_client = boto3.client("iot-data")

    def get_thing_connectivity(self, thing_name: str):
        try:
            kwargs = dict(queryString=f"thingName:{thing_name} AND connectivity.connected:*")
            response = self.iotthings_client.search_index(**kwargs)
            filtered_response = filter_thing_index_search(
                parameters=["thingTypeName", "attributes", "thingId"], results=response["things"]
            )
            return response["things"][0]["connectivity"]
        except Exception:
            logger.error("Error querying AWS Iot Thing connectivity message...")
            logger.error(traceback.format_exc())
            return False

    def get_thing_connectivity_bulk(self, organization_id: str, things: list):
        search_results = list()
        query = "connectivity.connected:* AND "
        if len(things) == 0:
            logger.error("No devices will be analyzed for connectivity...")
            return search_results

        for thing in things:
            query = query + f"thingName:{organization_id}---{thing}"
            if thing != things[-1]:
                query = query + " OR "
        kwargs = dict(queryString=query, maxResults=200)
        logger.info(kwargs)
        while True:
            response = self.iotthings_client.search_index(**kwargs)
            filtered_response = filter_thing_index_search(
                parameters=["thingTypeName", "attributes", "thingId", "shadow"], results=response["things"]
            )
            search_results.extend(filtered_response)
            if "nextToken" in response:
                kwargs["nextToken"] = response["nextToken"]
            else:
                break
        return search_results

    def get_things_connectivity(self):
        try:
            search_results = list()
            kwargs = dict(queryString="connectivity.connected:*", maxResults=200)
            while True:
                response = self.iotthings_client.search_index(**kwargs)
                filtered_response = filter_thing_index_search(
                    parameters=["shadow", "thingGroupNames"], results=response["things"]
                )
                search_results.extend(filtered_response)
                if "nextToken" in response:
                    kwargs["nextToken"] = response["nextToken"]
                else:
                    break
            return search_results
        except Exception:
            logger.error("Error querying AWS Iot Thing connectivity message...")
            logger.error(traceback.format_exc())
            return False

    def get_things_shadow(self, thing_name: str, shadow_name=None):
        try:
            kwargs = dict(thingName=thing_name)
            if shadow_name is not None:
                kwargs["shadowName"] = shadow_name
            response = self.iotthings_data_client.get_thing_shadow(**kwargs)
            return response
        except Exception:
            logger.error(f"Error getting thing shadow - {thing_name} - {shadow_name}")
            logger.error(traceback.format_exc())
            return False

    def get_things_shadow_enrich(self, organization_id: str, thing_list: list):
        results = list()
        for thing in thing_list:
            try:
                kwargs = dict(thingName=f"{organization_id}---{thing['id']}")
                response = self.iotthings_data_client.get_thing_shadow(**kwargs)
                response = self.shadow_streaming_body_parser(response)
                thing["hotData"] = response
                results.append(thing)
            except Exception:
                logger.error(f"Error getting thing shadow - {thing['id']}")
                logger.error(traceback.format_exc())
                results.append(thing)

        return results

    def advanced_index_query(self, organization_id: str, parameters: list):
        """
        :param organization_id:
        :param parameters: [{"parameter": "", "value": "", "operator": ""}]
        :return:
        """
        base_query = str()
        if len(parameters) >= 5:
            logger.error(f"Maximum number of queries in request exceeded... - {parameters}")
            return False

        serial_number_requests = [parameter["parameter"] for parameter in parameters if parameter["parameter"] == "serial_number" ]
        if len(serial_number_requests) > 1:
            logger.error(f"More than 1 device SN used as parameter... - {parameters}")
            return False

        for parameter in parameters:
            element_operator = parameter["operator"]
            if parameter["parameter"] == "serial_number":
                element_value = f"{organization_id}---{parameter['value']}"
            else:
                element_value = parameter["value"]

            for fixed_parameter in IOT_ANALYTICS_HOT_PATH_SEARCH_MAPPING:
                if fixed_parameter["parameter"] == parameter["parameter"]:
                    base_query = base_query + fixed_parameter["value"].format(
                        operator=element_operator, value=element_value
                    )
                    if parameter != parameters[-1]:
                        # Only one serial number at the time is allowed
                        if parameter["parameter"] == "serial_number":
                            base_query = base_query + " AND "
                        else:
                            base_query = base_query + " AND "

        try:
            search_results = list()
            print(base_query)
            kwargs = dict(queryString=base_query, maxResults=200)
            while True:
                response = self.iotthings_client.search_index(**kwargs)
                filtered_response = filter_thing_index_search(
                    parameters=["thingTypeName", "attributes", "thingId", "shadow"], results=response["things"]
                )
                search_results.extend(filtered_response)
                if "nextToken" in response:
                    kwargs["nextToken"] = response["nextToken"]
                else:
                    break
            return search_results

        except Exception:
            logger.error("Error querying AWS Iot Thing connectivity message...")
            logger.error(traceback.format_exc())
            return False

    @staticmethod
    def shadow_streaming_body_parser(shadow: dict):
        try:
            parsed_body = json.loads(shadow["payload"].read().decode())
            return parsed_body
        except Exception:
            logger.error("Error parsing shadow Streaming Body...")
            logger.error(shadow)
            logger.error(traceback.format_exc())
            return False


if __name__ == "__main__":
    iot_handler = IotThingsHandler()
    # test_results = iot_handler.get_things_shadow(thing_name="multa-agent-compose-i386-1-3")
    # print(iot_handler.shadow_streaming_body_parser(test_results))

    # result = iot_handler.get_thing_connectivity_bulk(things=["multa-agent-compose-i386-1-2", "multa-agent-compose-i386-1-3"])
    # print(result)

    parameters = [
        {
            "parameter": "serial_number",
            "operator": ":",
            "value": "agent-1-3"
        },
        {
            "parameter": "serial_number",
            "operator": ":",
            "value": "agent-1"
        }
    ]
    organization_id = "84b0882c-d474-4eb6-9838-416bdc68892a"
    query_results = iot_handler.advanced_index_query(organization_id=organization_id, parameters=parameters)
    print(query_results)
