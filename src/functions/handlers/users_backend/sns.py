from datetime import datetime
import json
import time
import traceback
import uuid

import boto3

from handlers.common import Sts
from settings.aws import USER_POOL_ID
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def generate_invite_url(email_address: str, organization_id: str):
    pass


class SnsHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.sns_client = boto3.client("sns")

    def send_message(self, email_data: dict):
        response = self.sns_client.list_users(UserPoolId=USER_POOL_ID, AttributesToGet=[], Limit=10,)
        if len(response["Users"]) == 1:
            return response["Users"]
        else:
            return False


if __name__ == "__main__":
    cognito_handler = SesHandler()
    user = cognito_handler.send_email(email_data={})
    logger.info(user)
