import json
import traceback

import boto3

from handlers.common import Sts
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

    def get_things_shadow_enrich(self, thing_list: list):
        results = list()
        for thing in thing_list:
            try:
                kwargs = dict(thingName=thing["id"])
                response = self.iotthings_data_client.get_thing_shadow(**kwargs)
                response = self.shadow_streaming_body_parser(response)
                thing["hotData"] = response
                results.append(thing)
            except Exception:
                logger.error(f"Error getting thing shadow - {thing['id']}")
                logger.error(traceback.format_exc())
                results.append(thing)

        return results

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
    test_results = iot_handler.get_things_shadow(thing_name="multa-agent-compose-i386-1-3")
    print(iot_handler.shadow_streaming_body_parser(test_results))
