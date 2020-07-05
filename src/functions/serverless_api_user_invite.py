import json
import traceback

from handlers.users_backend.ses import generate_invite_url, SesHandler
from handlers.users_backend.cognito import CognitoHandler
from handlers.users_backend.models import Organizations
from handlers.utils import base_response

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get(event, **kwargs):
    pass


def post(event, **kwargs):
    try:
        body = json.loads(event["body"])
        cognito_user_email = body["emailAddress"]
        user_organization_id = body["organizationId"]
        organization_data = Organizations.get_record_by_id(id_=user_organization_id)
        if organization_data is False:
            return False

        cognito_handler = CognitoHandler()
        is_email_valid = cognito_handler.check_user(email_address=cognito_user_email)
        if is_email_valid is not False:
            return False

        invite_url = generate_invite_url(email_address=cognito_user_email, organization_id=user_organization_id)
        ses_handler = SesHandler()
        email_sent = ses_handler.send_invite_email(invite_url=invite_url, recipient=cognito_user_email)
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
        "resource": "/users",
        "path": "/users/",
        "httpMethod": "POST",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Token eyJraWQiOiJBUTcrbDNJT2ZGZzhjSHN5dDExMlwvR3BSWEM4VHV4SUtiK1pqSGd2MFpmcz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlY2MxZTM0NC0xMDBlLTRiZTUtOWQ2NS1kYTlmMTk4YmRmMjIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfRHRXUzBqWW44IiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjpmYWxzZSwiY29nbml0bzp1c2VybmFtZSI6ImVjYzFlMzQ0LTEwMGUtNGJlNS05ZDY1LWRhOWYxOThiZGYyMiIsImdpdmVuX25hbWUiOiJFdWdlbmlvIiwiYXVkIjoiYWxpaTU4MDQxazcyaGh0OGdiN3IyY2duMiIsImV2ZW50X2lkIjoiOTQ1MTNlNTctNjA1Yi00YmVmLWFiOWYtNDU1ODZiNGYwZWI4IiwidXBkYXRlZF9hdCI6MTU5MjQ1NzUyOTczMCwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE1OTI1MzQ2NjYsInBob25lX251bWJlciI6IisxNzg2Njc1ODA1NCIsImV4cCI6MTU5MjUzODI2NiwiaWF0IjoxNTkyNTM0NjY2LCJmYW1pbHlfbmFtZSI6IkJyZWlqbyIsImVtYWlsIjoiZWViZjE5OTNAZ21haWwuY29tIn0.F_wBJTMlWEFMmL3pcjEyCHwo3J-5JmjMK5lzvANsw9vSsuMDe7SvSqIijmQf8k4rPql2FIE9zStaekyV7DdxBpg7la1Lvytt0b-8xkFTGHJE9MadURrk1kxRiYJP6yfyQQsET43HvTxb_LQzMw6f2JGOYGYrlThZ1-PlH_ftHfwZwVjwAYsihEPpaNAUFxiReqBJ8WcjQL3Tfirz9ON06Pxt4wu7BU1fwkFDJPxSlnUpsrPp-Q4OkmXsfgQHFIxo3SoHtUITui3WifJhAwinAdI9IbvMHRG4QqZCt_rgi2cVL7mdwwLZbJNIY02F0fBpoQEV76UUz6PYe1aKz60b4A",
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
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
            "Via": "2.0 0c9159c06691f6f55df2ceb396d9fd79.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "d4JSz3NDLcYbSH59oVzPi3QLkupJkNATzRLKkP7kCxQU9FgeTz4Arw==",
            "X-Amzn-Trace-Id": "Root=1-5eec2691-660d1a1db186375384de5b45",
            "X-Forwarded-For": "134.56.152.161, 52.46.25.102",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["application/json, text/plain, */*"],
            "Accept-Encoding": ["gzip, deflate, br"],
            "Accept-Language": ["en-US,en;q=0.9"],
            "Authorization": [
                "Token eyJraWQiOiJBUTcrbDNJT2ZGZzhjSHN5dDExMlwvR3BSWEM4VHV4SUtiK1pqSGd2MFpmcz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlY2MxZTM0NC0xMDBlLTRiZTUtOWQ2NS1kYTlmMTk4YmRmMjIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfRHRXUzBqWW44IiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjpmYWxzZSwiY29nbml0bzp1c2VybmFtZSI6ImVjYzFlMzQ0LTEwMGUtNGJlNS05ZDY1LWRhOWYxOThiZGYyMiIsImdpdmVuX25hbWUiOiJFdWdlbmlvIiwiYXVkIjoiYWxpaTU4MDQxazcyaGh0OGdiN3IyY2duMiIsImV2ZW50X2lkIjoiOTQ1MTNlNTctNjA1Yi00YmVmLWFiOWYtNDU1ODZiNGYwZWI4IiwidXBkYXRlZF9hdCI6MTU5MjQ1NzUyOTczMCwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE1OTI1MzQ2NjYsInBob25lX251bWJlciI6IisxNzg2Njc1ODA1NCIsImV4cCI6MTU5MjUzODI2NiwiaWF0IjoxNTkyNTM0NjY2LCJmYW1pbHlfbmFtZSI6IkJyZWlqbyIsImVtYWlsIjoiZWViZjE5OTNAZ21haWwuY29tIn0.F_wBJTMlWEFMmL3pcjEyCHwo3J-5JmjMK5lzvANsw9vSsuMDe7SvSqIijmQf8k4rPql2FIE9zStaekyV7DdxBpg7la1Lvytt0b-8xkFTGHJE9MadURrk1kxRiYJP6yfyQQsET43HvTxb_LQzMw6f2JGOYGYrlThZ1-PlH_ftHfwZwVjwAYsihEPpaNAUFxiReqBJ8WcjQL3Tfirz9ON06Pxt4wu7BU1fwkFDJPxSlnUpsrPp-Q4OkmXsfgQHFIxo3SoHtUITui3WifJhAwinAdI9IbvMHRG4QqZCt_rgi2cVL7mdwwLZbJNIY02F0fBpoQEV76UUz6PYe1aKz60b4A"
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
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
            ],
            "Via": ["2.0 0c9159c06691f6f55df2ceb396d9fd79.cloudfront.net (CloudFront)"],
            "X-Amz-Cf-Id": ["d4JSz3NDLcYbSH59oVzPi3QLkupJkNATzRLKkP7kCxQU9FgeTz4Arw=="],
            "X-Amzn-Trace-Id": ["Root=1-5eec2691-660d1a1db186375384de5b45"],
            "X-Forwarded-For": ["134.56.152.161, 52.46.25.102"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": "None",
        "multiValueQueryStringParameters": "None",
        "pathParameters": "None",
        "stageVariables": "None",
        "requestContext": {
            "resourceId": "ovux92",
            "authorizer": {
                "number": "1",
                "bool": "true",
                "principalId": "9aaa508c-511d-4a09-91e2-1a44e1804d57",
                "integrationLatency": 1083,
                "key": "value",
            },
            "resourcePath": "/user-invite",
            "httpMethod": "POST",
            "extendedRequestId": "OWr2yGyeoAMFZEA=",
            "requestTime": "19/Jun/2020:02:44:33 +0000",
            "path": "/prod/users/",
            "accountId": "112646120612",
            "protocol": "HTTP/1.1",
            "stage": "prod",
            "domainPrefix": "2qoob0tpqb",
            "requestTimeEpoch": 1592534673702,
            "requestId": "eb0b082e-5b3e-441d-92d3-e271d96f4443",
            "identity": {
                "cognitoIdentityPoolId": "None",
                "accountId": "None",
                "cognitoIdentityId": "None",
                "caller": "None",
                "sourceIp": "134.56.152.161",
                "principalOrgId": "None",
                "accessKey": "None",
                "cognitoAuthenticationType": "None",
                "cognitoAuthenticationProvider": "None",
                "userArn": "None",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                "user": "None",
            },
            "domainName": "2qoob0tpqb.execute-api.us-east-1.amazonaws.com",
            "apiId": "2qoob0tpqb",
        },
        "body": "None",
        "isBase64Encoded": False,
    }
    lambda_handler(event=lambda_event, context={})
