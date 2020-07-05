import boto3
import os
import time

from handlers.aws import get_object_from_bucket
from handlers.models import ServiceTokens


def lambda_handler(event, context):
    activation_time = round(time.time())
    print(event)

    # LAMBDA INVOKED BY TRIGGER THAT SENT EVENT -> EVENT CONTAINS BUCKET/ACTION -> START FLOW BASED ON ACTION
    object_bucket = os.environ["BUCKET"]
    environment = os.environ["ENVIRONMENT"]
    object_action = os.environ["ACTION"]

    # GET PLAN DATA FROM S3
    object_bucket_data = get_object_from_bucket(
        bucket_key=object_bucket, environment=environment, bucket_value=object_action
    )
    desired_service_tokens = object_bucket_data["service_tokens"]["values"]
    modified_service_tokens_ids = [
        desired_service_token.get("id")
        for desired_service_token in desired_service_tokens
        if desired_service_token.get("id") is not None
    ]
    modified_service_tokens = [
        desired_service_token
        for desired_service_token in desired_service_tokens
        if desired_service_token.get("id") is not None
    ]
    desired_new_service_tokens = [
        desired_service_token
        for desired_service_token in desired_service_tokens
        if desired_service_token.get("id") is None
    ]

    # GET PLAN DATA FROM DYNAMO
    record_service_tokens, total_service_tokens, service_tokens_last_evaluated_key = ServiceTokens.get_records()
    print(record_service_tokens)
    current_service_tokens = ServiceTokens.records_to_dict(record_service_tokens)

    # COMPARE PLAN DATA TO SEE IF PLAN HAS BEEN REMOVED FROM S3 COMPARED TO DYNAMO (USE IDs)
    current_service_tokens_ids = [current_service_token["id"] for current_service_token in current_service_tokens]

    desired_old_service_tokens_ids = set(current_service_tokens_ids) - set(modified_service_tokens_ids)

    # REMOVE FROM DYNAMO UNDESIRED PLANS
    for old_service_token_id in desired_old_service_tokens_ids:
        service_token = ServiceTokens.delete_record_by_id(old_service_token_id)

    # GET NEW PLANS (PLANS WITHOUT ID)
    for service_token in desired_new_service_tokens:
        new_service_token = ServiceTokens.create()

    # GO THRU ALL IN S3, IF EXIST IN DYNAMO -> UPDATE, IF NOT EXIST -> CREATE (USE IDs)
    for modified_service_token in modified_service_tokens:
        service_token = ServiceTokens.create(
            id_=modified_service_token["id"],
            value=modified_service_token["value"],
            is_valid=modified_service_token["is_valid"],
            created_time=modified_service_token["created_time"],
        )

    return {"time": activation_time, "status": 200}


if __name__ == "__main__":
    lambda_handler(event={}, context={})
