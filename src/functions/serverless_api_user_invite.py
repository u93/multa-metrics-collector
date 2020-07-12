import traceback

from handlers.users_backend.ses import generate_invite_url, SesHandler
from handlers.users_backend.cognito import CognitoHandler
from handlers.users_backend.models import UserOrganizationRelation
from handlers.utils import base_response, ApiGwEventParser

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get(event, **kwargs):
    pass


def post(event, **kwargs):
    try:
        request_parser = ApiGwEventParser(event=event)
        request_parser.parse()

        logger.info(request_parser.user_id)
        user_organization_mapping = UserOrganizationRelation.get_record_by_id(id_=request_parser.user_id)
        if user_organization_mapping is False:
            logger.error("Error getting current user info...")
            return False
        user_organization = user_organization_mapping.to_dict()["organizationId"]

        cognito_user_email = request_parser.body["emailAddress"]
        cognito_handler = CognitoHandler()
        is_email_valid = cognito_handler.check_user(email_address=cognito_user_email)
        if is_email_valid is not False:
            return False

        invite_url = generate_invite_url(email_address=cognito_user_email, organization_id=user_organization)
        ses_handler = SesHandler()
        email_sent = ses_handler.send_invite_email(invite_url=invite_url, recipient=cognito_user_email)
        logger.info(email_sent)
        if email_sent is False:
            return False

    except Exception:
        logger.error("Error GETTING current USER/ORGANIZATION and sending EMAIL for INVITE")
        logger.error(traceback.format_exc())
        return False

    return True


def put():
    pass


def patch():
    pass


def delete():
    pass


def lambda_handler(event, context):
    logger.info(event)

    http_method = event["httpMethod"]
    if http_method == "POST":
        current_info = post(event=event)
        if current_info is False:
            return base_response(status_code=500, dict_body=dict(results=False, error="Error inviting user..."))
        logger.info(dict(results=current_info))
        return base_response(status_code=200, dict_body=dict(results=dict(data=current_info)))

    else:
        return base_response(status_code=400, dict_body=dict(results=False, error="Unhandled method..."))


if __name__ == "__main__":
    lambda_event = {
        "resource": "/user-invite",
        "path": "/user-invite/",
        "httpMethod": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": "Token eyJraWQiOiJUM3FxbzZBSmNLelVQTENcL2NIcWsrZ0NwXC9KOFltUGRhNjZwTXRQOTRJVUk9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1OGFkNDY4Yi1iYjNjLTRiMmUtYjdiMS04MzU1OTZkMDBiZDEiLCJldmVudF9pZCI6IjMyZTdlN2I4LTZmOWUtNDhkYy05OGI2LTc1ZGFiNGViZGYxNCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTM5ODkwOTIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzN5MlpWTGFKSSIsImV4cCI6MTU5Mzk5MjY5MiwiaWF0IjoxNTkzOTg5MDkyLCJqdGkiOiJhYWQ5MjNmOS1mZGVmLTRhNmYtYjY2NC0xZTBjNGU0MjA1YjUiLCJjbGllbnRfaWQiOiI0dmcycGE3c3U3bWk0ZTRidWVtYWI3dnV2bCIsInVzZXJuYW1lIjoiNThhZDQ2OGItYmIzYy00YjJlLWI3YjEtODM1NTk2ZDAwYmQxIn0.iWfmmg57Pg6Ed4RDncdKfQKvpT74uCatP_Ad8ssp5Rg04LfE_swRk1ZI6DsLjhHOcK0ip7rZvcBC2EBh9ISsbSM1uB9L0EluLt3SG_rXmIusut-TQLL9tTj3w95MoLFBOjldhlTY00mgPg7AzBsnlGCU9wRJ-0ymkjhln2a4p7YWDAGAMDbdTIDK0FbtWE-plEBKBFztS0AnkzIQscfNE8KPGdxHS2fpvtqQ6u3iWqdt_Z14lNgCh2EiYtjju0amLO5aUmO5cUW6Td3YcYxzhzgzaUyCz0huQ74oTDKD4L9vb92NHMopjYePUwX9H2RbxoighG7iIZfVZpGMtlkm0A",
            "Cache-Control": "no-cache",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Content-Type": "application/json",
            "Host": "2qoob0tpqb.execute-api.us-east-1.amazonaws.com",
            "Postman-Token": "bbe209e7-65bd-436b-8ed4-a48eb6ec2516",
            "User-Agent": "PostmanRuntime/7.26.1",
            "Via": "1.1 2f003521460ce460cb069e0d2b93e692.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "1aqsj72IOY_eLzGi39ErJgJ70ecTMjRdDYa1KtsP8Xf6NStW_pe2hQ==",
            "X-Amzn-Trace-Id": "Root=1-5f025829-2d54049cf91f7a7c3e45f3a8",
            "X-Forwarded-For": "134.56.152.161, 52.46.25.152",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Accept-Encoding": ["gzip, deflate, br"],
            "Authorization": [
                "Token eyJraWQiOiJUM3FxbzZBSmNLelVQTENcL2NIcWsrZ0NwXC9KOFltUGRhNjZwTXRQOTRJVUk9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1OGFkNDY4Yi1iYjNjLTRiMmUtYjdiMS04MzU1OTZkMDBiZDEiLCJldmVudF9pZCI6IjMyZTdlN2I4LTZmOWUtNDhkYy05OGI2LTc1ZGFiNGViZGYxNCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTM5ODkwOTIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xXzN5MlpWTGFKSSIsImV4cCI6MTU5Mzk5MjY5MiwiaWF0IjoxNTkzOTg5MDkyLCJqdGkiOiJhYWQ5MjNmOS1mZGVmLTRhNmYtYjY2NC0xZTBjNGU0MjA1YjUiLCJjbGllbnRfaWQiOiI0dmcycGE3c3U3bWk0ZTRidWVtYWI3dnV2bCIsInVzZXJuYW1lIjoiNThhZDQ2OGItYmIzYy00YjJlLWI3YjEtODM1NTk2ZDAwYmQxIn0.iWfmmg57Pg6Ed4RDncdKfQKvpT74uCatP_Ad8ssp5Rg04LfE_swRk1ZI6DsLjhHOcK0ip7rZvcBC2EBh9ISsbSM1uB9L0EluLt3SG_rXmIusut-TQLL9tTj3w95MoLFBOjldhlTY00mgPg7AzBsnlGCU9wRJ-0ymkjhln2a4p7YWDAGAMDbdTIDK0FbtWE-plEBKBFztS0AnkzIQscfNE8KPGdxHS2fpvtqQ6u3iWqdt_Z14lNgCh2EiYtjju0amLO5aUmO5cUW6Td3YcYxzhzgzaUyCz0huQ74oTDKD4L9vb92NHMopjYePUwX9H2RbxoighG7iIZfVZpGMtlkm0A"
            ],
            "Cache-Control": ["no-cache"],
            "CloudFront-Forwarded-Proto": ["https"],
            "CloudFront-Is-Desktop-Viewer": ["true"],
            "CloudFront-Is-Mobile-Viewer": ["false"],
            "CloudFront-Is-SmartTV-Viewer": ["false"],
            "CloudFront-Is-Tablet-Viewer": ["false"],
            "CloudFront-Viewer-Country": ["US"],
            "Content-Type": ["application/json"],
            "Host": ["2qoob0tpqb.execute-api.us-east-1.amazonaws.com"],
            "Postman-Token": ["bbe209e7-65bd-436b-8ed4-a48eb6ec2516"],
            "User-Agent": ["PostmanRuntime/7.26.1"],
            "Via": ["1.1 2f003521460ce460cb069e0d2b93e692.cloudfront.net (CloudFront)"],
            "X-Amz-Cf-Id": ["1aqsj72IOY_eLzGi39ErJgJ70ecTMjRdDYa1KtsP8Xf6NStW_pe2hQ=="],
            "X-Amzn-Trace-Id": ["Root=1-5f025829-2d54049cf91f7a7c3e45f3a8"],
            "X-Forwarded-For": ["134.56.152.161, 52.46.25.152"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "2j03vq",
            "authorizer": {
                "number": "1",
                "bool": "true",
                "principalId": "861f25ab-3b36-4d4d-bc35-586309e0fe93",
                "integrationLatency": 920,
                "key": "value",
            },
            "resourcePath": "/user-invite",
            "httpMethod": "POST",
            "extendedRequestId": "POK2eEnioAMFuUA=",
            "requestTime": "05/Jul/2020:22:46:01 +0000",
            "path": "/prod/user-invite/",
            "accountId": "112646120612",
            "protocol": "HTTP/1.1",
            "stage": "prod",
            "domainPrefix": "2qoob0tpqb",
            "requestTimeEpoch": 1593989161322,
            "requestId": "e9849d9c-f5ac-496b-be6a-b4491e48c62f",
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
            "domainName": "2qoob0tpqb.execute-api.us-east-1.amazonaws.com",
            "apiId": "2qoob0tpqb",
        },
        "body": '{\n    "emailAddress": "eugeniobreijo2016@gmail.com",\n    "organizationId": "90856bba-45a5-49de-ab09-51361fcc276e"\n}',
        "isBase64Encoded": False,
    }
    response = lambda_handler(event=lambda_event, context={})
    logger.info(response)
