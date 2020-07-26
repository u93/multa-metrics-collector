import time

from handlers.backend.models import Devices
from handlers.devices.aws import ThingHandlers
from handlers.devices.registration import CvmRegistration
from handlers.middleware.api_validation import ApiGwEventParser, base_response
from handlers.middleware.device_validation import RegisterThingSchema
from settings.devices import THING_TYPE_NAME_RULE
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def lambda_handler(event, context):
    logger.info(event)

    http_method = event["httpMethod"]
    if http_method == "GET":
        return base_response(status_code=200, dict_body={"response": "OK"})

    if http_method == "POST":
        request_parser = ApiGwEventParser(event=event)
        request_parser.parse()

        request_body = request_parser.body
        organization_id = request_parser.authorizer_context["organizationId"]

        thing_handler = ThingHandlers()
        thing_type = thing_handler.get_thing_type(partial_name=THING_TYPE_NAME_RULE)
        if thing_type is False:
            return base_response(status_code=500, dict_body={"message": "Unable to register thing", "failureCode": "2"})
        thing_name = request_body["thingName"]
        thing_attributes = dict(
            attributes=dict(
                version=request_body["version"], organization_id=organization_id, creation_timestamp=str(round(time.time())),
            )
        )
        registration_payload = dict(
            thing_name=thing_name, thing_type_name=thing_type, thing_attributes=thing_attributes,
        )

        # Validating if request has valid parameters
        register_thing_schema = RegisterThingSchema()
        errors = register_thing_schema.validate(registration_payload)
        if errors:
            logger.info(errors)
            return base_response(status_code=400, dict_body={"message": str(errors), "failureCode": "3"})

        # Registering IoT Thing in AWS IoT
        thing_handler = CvmRegistration(thing_data=registration_payload)
        registration_response, registration_code = thing_handler.register_thing()
        if registration_response is False:
            return base_response(
                status_code=500, dict_body={"message": "Unable to register thing", "failureCode": registration_code}
            )

        registered_device = Devices.create(device_name=thing_name, organization_id=organization_id)
        if registered_device is False:
            return base_response(
                status_code=500, dict_body={"message": "Unable to register thing in database", "failureCode": registration_code}
            )

        response = {
            "certificates": registration_response["certificate_data"],
            "rootCA": registration_response["root_ca"],
            "failureCode": registration_code,
        }
        return base_response(status_code=200, dict_body=response, cors=False)


if __name__ == "__main__":
    event_data = {
        "resource": "/multa-agent",
        "path": "/multa-agent/",
        "httpMethod": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": "ApiKey b2998f5c31be35a98470858a2a893c55e1b8a1145318cda3a9f40df8cfcff8e9",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "Host": "cvm-agent.dev.multa.io",
            "Postman-Token": "bd83d51a-1975-4b66-b929-8b684704a26e",
            "User-Agent": "PostmanRuntime/7.26.1",
            "X-Amzn-Trace-Id": "Root=1-5f14ef73-53a851388620247810efffb0",
            "X-Forwarded-For": "134.56.152.161",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Accept-Encoding": ["gzip, deflate, br"],
            "Authorization": ["ApiKey b2998f5c31be35a98470858a2a893c55e1b8a1145318cda3a9f40df8cfcff8e9"],
            "Cache-Control": ["no-cache"],
            "Content-Type": ["application/json"],
            "Host": ["cvm-agent.dev.multa.io"],
            "Postman-Token": ["bd83d51a-1975-4b66-b929-8b684704a26e"],
            "User-Agent": ["PostmanRuntime/7.26.1"],
            "X-Amzn-Trace-Id": ["Root=1-5f14ef73-53a851388620247810efffb0"],
            "X-Forwarded-For": ["134.56.152.161"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "iey8bl",
            "authorizer": {
                "organizationId": "0d8ce688-07d1-439e-a1e7-2ca721e901e4",
                "apiKey": "b2998f5c31be35a98470858a2a893c55e1b8a1145318cda3a9f40df8cfcff8e9",
                "principalId": "b2998f5c31be35a98470858a2a893c55e1b8a1145318cda3a9f40df8cfcff8e9",
                "integrationLatency": 3164,
            },
            "resourcePath": "/multa-agent",
            "httpMethod": "POST",
            "extendedRequestId": "P8paEFqOoAMFRCQ=",
            "requestTime": "20/Jul/2020:01:12:19 +0000",
            "path": "/multa-agent/",
            "accountId": "112646120612",
            "protocol": "HTTP/1.1",
            "stage": "prod",
            "domainPrefix": "cvm-agent",
            "requestTimeEpoch": 1595207539532,
            "requestId": "1a8aae3d-ce95-495c-8ec2-87447f7fe9cc",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "sourceIp": "134.56.152.161",
                "principalOrgId": None,
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "PostmanRuntime/7.26.1",
                "user": None,
            },
            "domainName": "cvm-agent.dev.multa.io",
            "apiId": "t1nyujsyc4",
        },
        "body": '{\n\t"thingName": "test124",\n\t"version": "0.0.1"\n}',
        "isBase64Encoded": False,
    }
    lambda_response = lambda_handler(event=event_data, context={},)
    logger.info(lambda_response)
