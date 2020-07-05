import boto3
import os
import time

from handlers.aws import get_object_from_bucket
from handlers.models import Roles, InternalRoleGroup


def lambda_handler(event, context):
    activation_time = round(time.time())
    print(event)

    # LAMBDA INVOKED BY TRIGGER THAT SENT EVENT -> EVENT CONTAINS BUCKET/ACTION -> START FLOW BASED ON ACTION
    object_bucket = os.environ["BUCKET"]
    environment = os.environ["ENVIRONMENT"]
    object_action = os.environ["ACTION"]

    # GET ROLE DATA FROM S3
    object_bucket_data = get_object_from_bucket(
        bucket_key=object_bucket, environment=environment, bucket_value=object_action
    )
    desired_roles = object_bucket_data["roles"]["values"]
    modified_roles_ids = [
        desired_role.get("id") for desired_role in desired_roles if desired_role.get("id") is not None
    ]
    modified_roles = [desired_role for desired_role in desired_roles if desired_role.get("id") is not None]
    desired_new_roles = [desired_role for desired_role in desired_roles if desired_role.get("id") is None]

    # GET ROLE DATA FROM DYNAMO
    record_roles, total_records, roles_last_evaluated_key = Roles.get_records()
    print(record_roles)
    current_roles = Roles.records_to_dict(record_roles)

    # COMPARE ROLE DATA TO SEE IF ROLE HAS BEEN REMOVED FROM S3 COMPARED TO DYNAMO (USE IDs)
    current_roles_ids = [current_role["id"] for current_role in current_roles]

    desired_old_roles_ids = set(current_roles_ids) - set(modified_roles_ids)

    # REMOVE FROM DYNAMO UNDESIRED ROLES
    for old_role_id in desired_old_roles_ids:
        role = Roles.delete_record_by_id(old_role_id)

    # GET NEW ROLES (ROLES WITHOUT ID)
    for role in desired_new_roles:
        logic_groups = list()
        for group in role["logic_groups"]:
            logic_groups.append(
                InternalRoleGroup(
                    rest_api_id=group["restApiId"],
                    stage=group["stage"],
                    method=group["method"],
                    resources=group["resources"],
                )
            )
        role = Roles.create(name=role["name"], index=role["index"], logic_groups=logic_groups,)

    # GO THRU ALL IN S3, IF EXIST IN DYNAMO -> UPDATE, IF NOT EXIST -> CREATE (USE IDs)
    for modified_role in modified_roles:
        logic_groups = list()
        for group in modified_role["logic_groups"]:
            logic_groups.append(
                InternalRoleGroup(
                    rest_api_id=group["restApiId"],
                    stage=group["stage"],
                    method=group["method"],
                    resources=group["resources"],
                )
            )
        role = Roles.create(
            id_=modified_role["id"],
            index=modified_role["index"],
            name=modified_role["name"],
            logic_groups=logic_groups,
        )

    return {"time": activation_time, "status": 200}


if __name__ == "__main__":
    lambda_handler(event={}, context={})
