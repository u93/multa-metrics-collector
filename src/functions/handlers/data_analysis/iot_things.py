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
        self.iotthingss_client = boto3.client("iot")

    def get_things_connectivity(self):
        try:
            search_results = list()
            kwargs = dict(queryString="connectivity.connected:*", maxResults=200)
            while True:
                response = self.iotthingss_client.search_index(**kwargs)
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


if __name__ == "__main__":
    iot_handler = IotThingsHandler()
    results = iot_handler.get_things_connectivity()
    print(results)
