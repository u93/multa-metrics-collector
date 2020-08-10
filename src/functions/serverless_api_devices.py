import traceback

from handlers.analytics.iot_analytics import get_pretty_hot_path_metrics_enrich
from handlers.analytics.iot_things_analytics import IotThingsHandler
from handlers.backend.models import UserOrganizationRelation, Devices
from handlers.middleware.api_validation import base_response, ApiGwEventParser

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get(event, **kwargs):
    try:
        request_parser = ApiGwEventParser(event=event)
        request_parser.parse()

        user_id = request_parser.user_id
        user_organization_mapping = UserOrganizationRelation.get_record_by_id(id_=user_id)
        if user_organization_mapping is False:
            logger.error("Error getting current devices info...")
            return False

        user_organization = user_organization_mapping.to_dict()["organizationId"]
        devices, total = Devices.get_records(organization_id=user_organization)
        devices = Devices.records_to_dict(devices)

        device_analytics_handler = IotThingsHandler()
        devices = device_analytics_handler.get_things_shadow_enrich(
            organization_id=user_organization, thing_list=devices
        )
        devices = get_pretty_hot_path_metrics_enrich(thing_list=devices)

        device_connectivity = device_analytics_handler.get_thing_connectivity_bulk(
            organization_id=user_organization, things=[device["id"] for device in devices]
        )
        for device in device_connectivity:
            for device_info in devices:
                if device_info["id"] == device["thingName"]:
                    device_info["connectionStatus"] = device["connectivity"]["connected"]

    except Exception:
        logger.error("Error GETTING current DEVICES info")
        logger.error(traceback.format_exc())
        return False

    return devices


def post(event, **kwargs):
    try:
        request_parser = ApiGwEventParser(event=event)
        request_parser.parse()

        user_id = request_parser.user_id
        user_organization_mapping = UserOrganizationRelation.get_record_by_id(id_=user_id)
        if user_organization_mapping is False:
            logger.error("Error getting current devices info...")
            return False

        user_organization = user_organization_mapping.to_dict()["organizationId"]
        devices, total = Devices.get_records(organization_id=user_organization)
        devices = Devices.records_to_dict(devices)

        device_analytics_handler = IotThingsHandler()
        devices = device_analytics_handler.get_things_shadow_enrich(
            organization_id=user_organization, thing_list=devices
        )
        devices = get_pretty_hot_path_metrics_enrich(thing_list=devices)

        request_body = request_parser.body
        filtered_devices = device_analytics_handler.advanced_index_query(
            organization_id=user_organization, parameters=request_body
        )
        if filtered_devices is False:
            logger.error("Error excuting advanced queries for current devices info...")
            return False

        filtered_devices = [device["thingName"] for device in filtered_devices]
        devices = [device for device in devices if f"{user_organization}---{device['id']}" in filtered_devices]
        device_connectivity = device_analytics_handler.get_thing_connectivity_bulk(
            organization_id=user_organization, things=[device["id"] for device in devices]
        )
        for device in device_connectivity:
            for device_info in devices:
                if device_info["id"] == device["thingName"]:
                    device_info["connectionStatus"] = device["connectivity"]["connected"]

    except Exception:
        logger.error("Error GETTING current DEVICES info")
        logger.error(traceback.format_exc())
        return False

    return devices


def put():
    pass


def patch():
    pass


def delete():
    pass


def lambda_handler(event, context):
    logger.info(event)

    http_method = event["httpMethod"]
    if http_method == "GET":
        current_info = get(event=event)
    elif http_method == "POST":
        current_info = post(event=event)
    else:
        return base_response(status_code=400, dict_body=dict(results=False, error="Unhandled method..."))

    if current_info is False:
        return base_response(status_code=500, dict_body=dict(results=False, error="Error getting device info..."))

    return base_response(status_code=200, dict_body=dict(results=dict(data=current_info)))


if __name__ == "__main__":
    lambda_event = {
        "resource": "/users",
        "path": "/users/",
        "httpMethod": "POST",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Token eyJraWQiOiJUM3FxbzZBSmNLelVQTENcL2NIcWsrZ0NwXC9KOFltUGRhNjZwTXRQOTRJVUk9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4NjFmMjVhYi0zYjM2LTRkNGQtYmMzNS01ODYzMDllMGZlOTMiLCJldmVudF9pZCI6ImEwNDhjMjllLTQ1NmMtNGY0Ni1iZGZhLTBhNGUyYjliZTY0ZCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTQyNjE5MTgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzN5MlpWTGFKSSIsImV4cCI6MTU5NDI2NTUxOCwiaWF0IjoxNTk0MjYxOTE4LCJqdGkiOiI3N2ExYTdhYy1hZGU0LTRjYzktODc3Yy1hZTA3ZTE2NjNiMmQiLCJjbGllbnRfaWQiOiI0dmcycGE3c3U3bWk0ZTRidWVtYWI3dnV2bCIsInVzZXJuYW1lIjoiODYxZjI1YWItM2IzNi00ZDRkLWJjMzUtNTg2MzA5ZTBmZTkzIn0.AjgiYy8fSXrsIlOq6sIbNJnEN1oRzB6Kbkx3btDSzJ5sDCipLqujOy8impw8vYts0wWaUJ5SrHjqoZvmXMj5LxSizpTG8ZEkohbEAYXEWGQW8U-oKNoN9XhbKz_WpwS-uCj34dlYaXrKcfb-6dNUVpkfoU5plL268W_PW8bRiKUu2YJrBSq6jn0_A8M2N2XDjwdaPdrC_j-6DQytX4TDWPpoGf3t29G6iJADKiJI4TYPsS_mc7A1lOajWnLXVwNGRXWvgNcbmyJ_mOi6cyF2_RHT-BGoYZZ7-V3OyFZb5tKBdw_ejpgi_MxXPkvNozH1Lm8ByYuDvzFF_GmX9TA00A",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "2qoob0tpqb.execute-api.us-east-1.amazonaws.com",
            "origin": "https://dev.d14258l1f04l0x.amplifyapp.com",
            "Referer": "https://dev.d14258l1f04l0x.amplifyapp.com/settings",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Via": "2.0 fc1009b8e45427207e2a571827e9dd24.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "KqnFZoWleZzYCfcsoCvdeBwGbZYJQhsShkJ8E33wE5ARX-t7tkCk5Q==",
            "X-Amzn-Trace-Id": "Root=1-5f0681a5-4d957e7484bf62e8e753141d",
            "X-Forwarded-For": "134.56.152.161, 64.252.129.146",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["application/json, text/plain, */*"],
            "Accept-Encoding": ["gzip, deflate, br"],
            "Accept-Language": ["en-US,en;q=0.9"],
            "Authorization": [
                "Token eyJraWQiOiJUM3FxbzZBSmNLelVQTENcL2NIcWsrZ0NwXC9KOFltUGRhNjZwTXRQOTRJVUk9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4NjFmMjVhYi0zYjM2LTRkNGQtYmMzNS01ODYzMDllMGZlOTMiLCJldmVudF9pZCI6ImEwNDhjMjllLTQ1NmMtNGY0Ni1iZGZhLTBhNGUyYjliZTY0ZCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTQyNjE5MTgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzN5MlpWTGFKSSIsImV4cCI6MTU5NDI2NTUxOCwiaWF0IjoxNTk0MjYxOTE4LCJqdGkiOiI3N2ExYTdhYy1hZGU0LTRjYzktODc3Yy1hZTA3ZTE2NjNiMmQiLCJjbGllbnRfaWQiOiI0dmcycGE3c3U3bWk0ZTRidWVtYWI3dnV2bCIsInVzZXJuYW1lIjoiODYxZjI1YWItM2IzNi00ZDRkLWJjMzUtNTg2MzA5ZTBmZTkzIn0.AjgiYy8fSXrsIlOq6sIbNJnEN1oRzB6Kbkx3btDSzJ5sDCipLqujOy8impw8vYts0wWaUJ5SrHjqoZvmXMj5LxSizpTG8ZEkohbEAYXEWGQW8U-oKNoN9XhbKz_WpwS-uCj34dlYaXrKcfb-6dNUVpkfoU5plL268W_PW8bRiKUu2YJrBSq6jn0_A8M2N2XDjwdaPdrC_j-6DQytX4TDWPpoGf3t29G6iJADKiJI4TYPsS_mc7A1lOajWnLXVwNGRXWvgNcbmyJ_mOi6cyF2_RHT-BGoYZZ7-V3OyFZb5tKBdw_ejpgi_MxXPkvNozH1Lm8ByYuDvzFF_GmX9TA00A"
            ],
            "CloudFront-Forwarded-Proto": ["https"],
            "CloudFront-Is-Desktop-Viewer": ["true"],
            "CloudFront-Is-Mobile-Viewer": ["false"],
            "CloudFront-Is-SmartTV-Viewer": ["false"],
            "CloudFront-Is-Tablet-Viewer": ["false"],
            "CloudFront-Viewer-Country": ["US"],
            "Host": ["2qoob0tpqb.execute-api.us-east-1.amazonaws.com"],
            "origin": ["https://dev.d14258l1f04l0x.amplifyapp.com"],
            "Referer": ["https://dev.d14258l1f04l0x.amplifyapp.com/settings"],
            "sec-fetch-dest": ["empty"],
            "sec-fetch-mode": ["cors"],
            "sec-fetch-site": ["cross-site"],
            "User-Agent": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
            ],
            "Via": ["2.0 fc1009b8e45427207e2a571827e9dd24.cloudfront.net (CloudFront)"],
            "X-Amz-Cf-Id": ["KqnFZoWleZzYCfcsoCvdeBwGbZYJQhsShkJ8E33wE5ARX-t7tkCk5Q=="],
            "X-Amzn-Trace-Id": ["Root=1-5f0681a5-4d957e7484bf62e8e753141d"],
            "X-Forwarded-For": ["134.56.152.161, 64.252.129.146"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "ovux92",
            "authorizer": {
                "number": "1",
                "bool": "true",
                "principalId": "861f25ab-3b36-4d4d-bc35-586309e0fe93",
                "integrationLatency": 857,
                "key": "value",
            },
            "resourcePath": "/users",
            "httpMethod": "GET",
            "extendedRequestId": "PYkx0FXjoAMFd3Q=",
            "requestTime": "09/Jul/2020:02:32:05 +0000",
            "path": "/prod/users/",
            "accountId": "112646120612",
            "protocol": "HTTP/1.1",
            "stage": "prod",
            "domainPrefix": "2qoob0tpqb",
            "requestTimeEpoch": 1594261925160,
            "requestId": "be9ec84b-2050-49d5-855f-9b3c4d9880ac",
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
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                "user": None,
            },
            "domainName": "2qoob0tpqb.execute-api.us-east-1.amazonaws.com",
            "apiId": "2qoob0tpqb",
        },
        "body": '[\n    {\n        "parameter": "serial_number",\n        "operator": ":",\n        "value": "agent-1-2"\n    },\n    {\n        "parameter": "ram_insights_status",\n        "operator": ":",\n        "value": false\n    }\n]',
        "isBase64Encoded": False,
    }
    response = lambda_handler(event=lambda_event, context={})
    print(response)
