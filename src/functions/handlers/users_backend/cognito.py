from datetime import datetime
import json
import time
import traceback
import uuid

import boto3

from handlers.common import Sts
from settings.aws import (
    USER_POOL_ID,
)
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def parse_user_attributes(attributes: list) -> dict:
    attribute_dict = dict()
    for attribute in attributes:
        if attribute["Name"] == "sub":
            attribute["Name"] = "id"
        attribute_dict[attribute["Name"]] = attribute["Value"]
    return attribute_dict


def parse_attributes(users_list: list):
    parsed_users = list()
    for user in users_list:
        attribute_dict = dict()
        for attribute in user["Attributes"]:
            if attribute["Name"] == "sub":
                attribute["Name"] = "id"
            attribute_dict[attribute["Name"]] = attribute["Value"]
        parsed_users.append(attribute_dict)

    return parsed_users


class CognitoHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.cognito_client = boto3.client("cognito-idp")

    def get_user_by_access_token(self, access_token):
        user_response = dict(user_id=None, user_attributes=None)
        try:
            response = self.cognito_client.get_user(
                AccessToken=access_token
            )
        except Exception:
            logger.error("Error GETTING USER by ACCESS Token")
            logger.error(traceback.format_exc())
            return False
        else:
            user_response["user_id"] = response["Username"]
            user_response["user_attributes"] = response["UserAttributes"]
            return user_response

    def check_user(self, email_address: str):
        response = self.cognito_client.list_users(
            UserPoolId=USER_POOL_ID,
            AttributesToGet=[],
            Limit=10,
            Filter=f"email = '{email_address}'"
        )
        if len(response["Users"]) == 1:
            return response["Users"]
        else:
            return False

    def list_users(self, pagination_token=None):
        kwargs = {
            "UserPoolId": USER_POOL_ID,
            "Limit": 20,
        }
        if pagination_token is not None:
            kwargs["PaginationToken"] = pagination_token
        response = self.cognito_client.list_users(**kwargs)
        return response


if __name__ == "__main__":
    cognito_handler = CognitoHandler()
    users = cognito_handler.list_users()
    logger.info(users)

    latest_users = parse_attributes(users["Users"])
    logger.info(latest_users)

    user_data = cognito_handler.get_user_by_access_token(access_token="eyJraWQiOiIzb2dCdmhmY3JGNVFlMnRXUW5oK2JnNjBleFFhVHdxZXZna04yVXpmcHhnPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NzU1NmQ0OS00MmI3LTRjZGUtYTY4MC1iMjI4OTZmOTk1Y2YiLCJldmVudF9pZCI6ImNiOWFkYmYwLWQxZjQtNDY3YS1iY2E3LTRjNjc0MTRjZmI4OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTI3ODkwNDUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0R0V1MwalluOCIsImV4cCI6MTU5Mjc5MjY0NSwiaWF0IjoxNTkyNzg5MDQ1LCJqdGkiOiI5MmYzODljMi1hMTI2LTQ3MjctODE2YS0xNGRhNGI4NDM5ZDAiLCJjbGllbnRfaWQiOiJhbGlpNTgwNDFrNzJoaHQ4Z2I3cjJjZ24yIiwidXNlcm5hbWUiOiI2NzU1NmQ0OS00MmI3LTRjZGUtYTY4MC1iMjI4OTZmOTk1Y2YifQ.BHpSTXcL6BXB00aZ7nN84qIGx6VId5wMu3tQHaS1FBNJRR7mSY4zr0FA8miFVH7EQ5NhagrUfTT9ch3EcsRGwvcm3BY8vF4Ejds04ToTFsD2g1QUZDlHyNS_xQh8TgoFM07qqNgBUfwfj8KaNrs_CeilVl_NtF_jFL5S8tlJPCGM7b69mAe51OV7M9ac8WIrM5r5hvzonYT3drb07_hbNy8GC5rcNdFUTukQUJhiKwzIyhNRIT9v7FfBHHzY12ZZ--YMzoEfH0WIen61ZIt917cHh6Wnpq2BjKjsklEX_yyk2IrGfQmBsfP9ofrPBD4rET30j5xs6nNanPyLBL7KXg")
    logger.info(user_data)