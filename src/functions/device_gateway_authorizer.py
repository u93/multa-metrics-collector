import logging
import traceback

from handlers.authorization.iam import AuthPolicy
from handlers.backend.models import Devices, Organizations, Plans
from handlers.middleware.device_validation import RegisterApiAuthSchema

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def lambda_handler(event, context):
    logging.info(event)
    logging.info("Client token: " + event["authorizationToken"])
    logging.info("Method ARN: " + event["methodArn"])

    try:
        register_schema = RegisterApiAuthSchema()
        data = register_schema.load(dict(authorizationToken=event["authorizationToken"]))
    except Exception:
        logger.error("Error validating Device Authorization data")
        logger.error(traceback.format_exc())
        raise Exception("Unauthorized")

    authorization_token = event["authorizationToken"].split()[1]
    api_key = Organizations.get_record_by_api_key(id_=authorization_token)
    if api_key is False:
        logger.error(f"API Key not found - {authorization_token}")
        raise Exception("Unauthorized")

    try:
        organization_id = api_key.to_dict()["id"]
        organization_plan = api_key.to_dict()["plan"]
    except Exception:
        logger.error(f"Error parsing Organization from API Key - {authorization_token}")
        logger.error(traceback.format_exc())
        raise Exception("Unauthorized")

    records_devices, total = Devices.get_records(organization_id=organization_id)
    logger.info(records_devices)
    if records_devices is False:
        logger.error(f"Error getting Organization devices... - {organization_id}")
        raise Exception("Unauthorized")

    devices = Devices.records_to_dict(records=records_devices)
    if devices is False:
        logger.error(f"Error getting parsing Organization devices... - {organization_id}")
        raise Exception("Unauthorized")

    plan_info = Plans.get_record_by_id(id_=organization_plan)
    if plan_info is False:
        logger.error("Error getting organization plan...")
        raise Exception("Unauthorized")

    maximum_number_agents = plan_info.to_dict()["conditions"]["numberOfAgentsDetail"]
    if len(devices) >= maximum_number_agents:
        logger.error("Maximum number of agents registered...")
        raise Exception("Unauthorized")

    principal_id = authorization_token
    tmp = event["methodArn"].split(":")
    api_gateway_arn_tmp = tmp[5].split("/")
    aws_account_id = tmp[4]

    policy = AuthPolicy(principal_id, aws_account_id)
    policy.rest_api_id = api_gateway_arn_tmp[0]
    policy.region = tmp[3]
    policy.stage = api_gateway_arn_tmp[1]

    if principal_id is None:
        policy.deny_all_methods()
    else:
        policy.allow_all_methods()

    auth_response = policy.build()
    auth_response["context"] = dict(
        apiKey=principal_id, organizationId=organization_id
    )  # $context.authorizer.key -> value

    return auth_response


if __name__ == "__main__":
    event_data = {
        "type": "TOKEN",
        "methodArn": "arn:aws:execute-api:us-east-1:112646120612:t1nyujsyc4/prod/POST/multa-agent/",
        "authorizationToken": "ApiKey fc369ce4dfa955d6781325e42b28a3480f4f338d916876f736f907bbcb2b7f8f",
    }
    response = lambda_handler(event=event_data, context={},)
