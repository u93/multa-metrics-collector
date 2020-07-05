import boto3
import os
import time

from handlers.aws import get_object_from_bucket
from handlers.models import Plans


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
    desired_plans = object_bucket_data["plans"]["values"]
    modified_plans_ids = [
        desired_plan.get("id") for desired_plan in desired_plans if desired_plan.get("id") is not None
    ]
    modified_plans = [desired_plan for desired_plan in desired_plans if desired_plan.get("id") is not None]
    desired_new_plans = [desired_plan for desired_plan in desired_plans if desired_plan.get("id") is None]

    # GET PLAN DATA FROM DYNAMO
    record_plans, total_records, plans_last_evaluated_key = Plans.get_records()
    print(record_plans)
    current_plans = Plans.records_to_dict(record_plans)

    # COMPARE PLAN DATA TO SEE IF PLAN HAS BEEN REMOVED FROM S3 COMPARED TO DYNAMO (USE IDs)
    current_plans_ids = [current_plan["id"] for current_plan in current_plans]

    desired_old_plans_ids = set(current_plans_ids) - set(modified_plans_ids)

    # REMOVE FROM DYNAMO UNDESIRED PLANS
    for old_plan_id in desired_old_plans_ids:
        plan = Plans.delete_record_by_id(old_plan_id)

    # GET NEW PLANS (PLANS WITHOUT ID)
    for plan in desired_new_plans:
        new_plan = Plans.create(name=plan["name"], conditions=plan["conditions"], price=plan["price"])

    # GO THRU ALL IN S3, IF EXIST IN DYNAMO -> UPDATE, IF NOT EXIST -> CREATE (USE IDs)
    for modified_plan in modified_plans:
        plan = Plans.create(
            id_=modified_plan["id"],
            name=modified_plan["name"],
            conditions=modified_plan["conditions"],
            price=modified_plan["price"],
        )

    return {"time": activation_time, "status": 200}


if __name__ == "__main__":
    lambda_handler(event={}, context={})
