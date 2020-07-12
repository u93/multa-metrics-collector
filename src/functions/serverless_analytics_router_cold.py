import json
# import os
import time

from handlers.analytics.lambda_functions import LambdaHandler
from handlers.utils import base_response
from settings.aws import ANALYTICS_LAMBDA_ROUTING_MAPPING
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def lambda_handler(event, context):
    activation_time = round(time.time())
    logger.info(activation_time)
    logger.info(event)
    logger.info(event["queryStringParameters"])
    logger.info(event["body"])

    request_qs_parameter = event.get("queryStringParameters", None)
    if request_qs_parameter is None:
        logger.error("Metric parameter not passed...")
        return base_response(status_code=400, dict_body=dict(result=False, error="Metric parameter not passed..."))

    desired_metric = request_qs_parameter.get("metric", None)
    if desired_metric is None:
        logger.error("Desired metric not passed...")
        return base_response(status_code=400, dict_body=dict(result=False, error="Desired metric not passed..."))

    request_body = event.get("body", None)
    if request_body is None:
        logger.error("Analysis parameters not passed...")
        return base_response(status_code=400, dict_body=dict(result=False, error="Analysis parameters not passed..."))

    function_name = ANALYTICS_LAMBDA_ROUTING_MAPPING.get(desired_metric, None)
    if function_name is None:
        logger.error("Metric analyzer not found...")
        return base_response(status_code=400, dict_body=dict(result=False, error="Metric analyzer not found..."))

    routing_handler = LambdaHandler()
    invoke_result = routing_handler.invoke(function_name=function_name, payload=request_body)

    return base_response(status_code=200, dict_body=dict(results=json.loads(invoke_result)))


if __name__ == "__main__":
    event = {
        "resource": "/cold",
        "path": "/cold/",
        "httpMethod": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": "Token",
            "Cache-Control": "no-cache",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Content-Type": "application/json",
            "Host": "iirchaax58.execute-api.us-east-1.amazonaws.com",
            "Postman-Token": "bf0fbf37-76ac-4a18-8167-4a501feb0bbe",
            "User-Agent": "PostmanRuntime/7.24.1",
            "Via": "1.1 daeaa56d606882a18020d4b2db149c16.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "8N5KkntqMou5dORoFdZYR-bu6v-wK82Mi7XznC1xGIJmY9P04v2bjA==",
            "X-Amzn-Trace-Id": "Root=1-5ecb3432-7010bdb07c5a73f416126efc",
            "X-Forwarded-For": "134.56.152.161, 70.132.5.137",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Accept-Encoding": ["gzip, deflate, br"],
            "Authorization": ["Token"],
            "Cache-Control": ["no-cache"],
            "CloudFront-Forwarded-Proto": ["https"],
            "CloudFront-Is-Desktop-Viewer": ["true"],
            "CloudFront-Is-Mobile-Viewer": ["false"],
            "CloudFront-Is-SmartTV-Viewer": ["false"],
            "CloudFront-Is-Tablet-Viewer": ["false"],
            "CloudFront-Viewer-Country": ["US"],
            "Content-Type": ["application/json"],
            "Host": ["iirchaax58.execute-api.us-east-1.amazonaws.com"],
            "Postman-Token": ["bf0fbf37-76ac-4a18-8167-4a501feb0bbe"],
            "User-Agent": ["PostmanRuntime/7.24.1"],
            "Via": ["1.1 daeaa56d606882a18020d4b2db149c16.cloudfront.net (CloudFront)"],
            "X-Amz-Cf-Id": ["8N5KkntqMou5dORoFdZYR-bu6v-wK82Mi7XznC1xGIJmY9P04v2bjA=="],
            "X-Amzn-Trace-Id": ["Root=1-5ecb3432-7010bdb07c5a73f416126efc"],
            "X-Forwarded-For": ["134.56.152.161, 70.132.5.137"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": {"metric": "connectivity"},
        "multiValueQueryStringParameters": {"metric": ["ram"]},
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "sth2rl",
            "authorizer": {
                "number": "1",
                "bool": "true",
                "principalId": "user|a1b2c3d4",
                "integrationLatency": 364,
                "key": "value",
            },
            "resourcePath": "/cold",
            "httpMethod": "POST",
            "extendedRequestId": "NEUX1FnToAMFv2g=",
            "requestTime": "25/May/2020:02:57:54 +0000",
            "path": "/prod/cold/",
            "accountId": "112646120612",
            "protocol": "HTTP/1.1",
            "stage": "prod",
            "domainPrefix": "iirchaax58",
            "requestTimeEpoch": 1590375474019,
            "requestId": "033a4215-858f-4a07-99b2-0d9208019141",
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
                "userAgent": "PostmanRuntime/7.24.1",
                "user": None,
            },
            "domainName": "iirchaax58.execute-api.us-east-1.amazonaws.com",
            "apiId": "iirchaax58",
        },
        "body": '{\n\t"analysis": "average",\n\t"parameters": {\n\t\t"metric_value": "123",\n\t\t"metric_range": "123",\n\t\t"start_time": "123",\n\t\t"end_time": "123",\n\t\t"start_date": "123",\n\t\t"end_date": "123",\n\t\t"start_timestamp": 123,\n\t\t"end_timestamp": 123,\n\t\t"agents": ["123", "123"],\n\t\t"metadata": {\n\t\t\t"key": "value"\n\t\t}\n\t}\n}',
        "isBase64Encoded": False,
    }
    lambda_handler(event=event, context={})
