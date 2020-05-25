import traceback

import boto3

from handlers.common import Sts
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


class LambdaHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.lambda_client = boto3.client("lambda")

    def invoke(self, function_name, payload):
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType="RequestResponse",
                Payload=payload,
            )

        except Exception:
            logger.error(f"Error invoking lambda function {function_name}")
            logger.error(traceback.format_exc())
            return False
        else:
            return response["Payload"].read()
