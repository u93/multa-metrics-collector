import traceback

from handlers.backend.cognito import CognitoHandler, parse_user_attributes
from handlers.backend.models import Organizations, Plans, Roles, UserOrganizationRelation, Users
from handlers.utils import base_response

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get(event, **kwargs):
    user_organization_data = dict(
        userInfo=dict(id=None, attributes=dict(), role=None, creationTime=None, lastUpdated=None),
        organizationInfo=dict(
            id=None, name=None, plan=None, owner=None, creationTime=None, lastUpdated=None, billingTime=None
        ),
    )
    try:
        user_id = event["requestContext"]["authorizer"]["principalId"]
        cognito_access_token = event["headers"]["Authorization"].split()[1]
        cognito_handler = CognitoHandler()
        user_data = cognito_handler.get_user_by_access_token(access_token=cognito_access_token)

        user_organization_relation_data = UserOrganizationRelation.get_record_by_id(id_=user_id)
        user_organization_id = user_organization_relation_data.to_dict()["organizationId"]

        user_info_data = Users.get_record_by_id(organization_id=user_organization_id, user_id=user_id)
        organization_data = Organizations.get_record_by_id(id_=user_organization_id)
        role_data = Roles.get_record_by_id(id_=user_info_data.to_dict()["role"])
        plan_data = Plans.get_record_by_id(id_=organization_data.to_dict()["plan"])

        user_organization_data["userInfo"]["id"] = user_id
        user_organization_data["userInfo"]["attributes"] = parse_user_attributes(user_data["user_attributes"])
        user_organization_data["userInfo"]["role"] = role_data.to_dict()
        user_organization_data["userInfo"]["creationTime"] = user_info_data.to_dict()["creationTime"]
        user_organization_data["userInfo"]["lastUpdated"] = user_info_data.to_dict()["lastUpdated"]

        user_organization_data["organizationInfo"]["id"] = user_organization_id
        user_organization_data["organizationInfo"]["name"] = organization_data.to_dict()["name"]
        user_organization_data["organizationInfo"]["plan"] = plan_data.to_dict()
        user_organization_data["organizationInfo"]["owner"] = organization_data.to_dict()["owner"]
        user_organization_data["organizationInfo"]["creationTime"] = organization_data.to_dict()["creationTime"]
        user_organization_data["organizationInfo"]["lastUpdated"] = organization_data.to_dict()["lastUpdated"]
        user_organization_data["organizationInfo"]["billingTime"] = organization_data.to_dict()["billingTime"]

    except Exception:
        logger.error("Error GETTING current USER/ORGANIZATION info")
        logger.error(traceback.format_exc())
        return False

    return user_organization_data


def post():
    pass


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
        if current_info is False:
            return base_response(
                status_code=500, dict_body=dict(results=False, error="Error getting user/organization info...")
            )
        return base_response(status_code=200, dict_body=dict(results=dict(data=current_info)))

    else:
        return base_response(status_code=400, dict_body=dict(results=False, error="Unhandled method..."))


if __name__ == "__main__":
    lambda_event = {
        "resource": "/users",
        "path": "/users/",
        "httpMethod": "GET",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Token eyJraWQiOiIzb2dCdmhmY3JGNVFlMnRXUW5oK2JnNjBleFFhVHdxZXZna04yVXpmcHhnPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NzU1NmQ0OS00MmI3LTRjZGUtYTY4MC1iMjI4OTZmOTk1Y2YiLCJldmVudF9pZCI6ImM1NTEyMjc3LWNkZmYtNGEwNi1hNGMzLTZmODAzOTFjNGQwZiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTM4MzQ0MzksImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0R0V1MwalluOCIsImV4cCI6MTU5MzgzODA0MCwiaWF0IjoxNTkzODM0NDQwLCJqdGkiOiJmYTMzMjg0ZS1iMWQ1LTQ5OGMtYTBkZi0zNjRmYmVmYmM2YzMiLCJjbGllbnRfaWQiOiJhbGlpNTgwNDFrNzJoaHQ4Z2I3cjJjZ24yIiwidXNlcm5hbWUiOiI2NzU1NmQ0OS00MmI3LTRjZGUtYTY4MC1iMjI4OTZmOTk1Y2YifQ.iWFw6INmntkEEneWAEIL2EGsAB9n93Pw3KbJIXMfqj7NbHnh0TPozHxW1n0ydY6rX80IV6lXmkRYkeSzdUXFKlMePd3MwbttBsMYT_kiAyuJbfEWDepfsdiZUT3QZ37ApS0uCq1cjySiLDNol4LDpjDR3_E4CoBOEQRdhVz2NAgvnaPH4sbsuVpv51Q8bZ3GYi957E1KQu3201XSMqTuRGvfbyDQt5-lHf6ulWxGNmSf789_usDyc5gsHeHb-YOg_Wwpzln1p5vIN1n6WoTh7ss98PZbRWbZp7SdeRsmoMEheJ_XKw-MI5sT4scdWf4q5F2oS04_uZeBgr-JVedtDw",
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
                "principalId": "67556d49-42b7-4cde-a680-b22896f995cf",
                "integrationLatency": 1083,
                "key": "value",
            },
            "resourcePath": "/users",
            "httpMethod": "GET",
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
    response = lambda_handler(event=lambda_event, context={})
    logger.info(response)
