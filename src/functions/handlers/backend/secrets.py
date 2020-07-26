import traceback

import boto3

from handlers.common import Sts
from settings.aws import SECRETS
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get_api_key_secret():
    handler = SecretsHandler()
    value = handler.get_secret_value(secret_name=SECRETS["SECRET_API_KEY"])
    return value


class SecretsHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.secrets_client = boto3.client("secretsmanager")

    def get_secret_value(self, secret_name: str):
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name,)
        except Exception:
            logger.error(f"Error getting secret - {secret_name}")
            logger.error(traceback.format_exc())
            return False
        else:
            return response["SecretString"]


if __name__ == "__main__":
    handler = SecretsHandler()
    value = handler.get_secret_value(secret_name="MULTA-METRICS-SECRETS/dev/API-KEY")
    logger.info(value)
