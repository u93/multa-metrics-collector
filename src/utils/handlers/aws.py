import json
import traceback

import boto3

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.logger


def get_object_from_bucket(bucket_key: str, environment: str, bucket_value: str):
    try:
        s3 = boto3.resource("s3")
        content_object = s3.Object(bucket_key, f"{environment}/{bucket_value}.json")
        file_content = content_object.get()["Body"].read().decode("utf-8")
        json_content = json.loads(file_content)
        return json_content
    except Exception:
        logger.error(f"Error getting {environment}/{bucket_value} object")
        logger.error(traceback.format_exc())
        return False
