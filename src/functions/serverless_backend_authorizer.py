import traceback

# from jose import jwk, jwt
# from jose.utils import base64url_decode

from handlers.authorization.iam import AuthPolicy
from handlers.backend.cognito import CognitoHandler
from handlers.backend.models import Roles, ServiceTokens

# from settings.aws import USER_POOL_APP_CLIENT_ID
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def validate_access_token(access_token: str):
    try:
        cognito_handler = CognitoHandler()
        user_data = cognito_handler.get_user_by_access_token(access_token=access_token)
        if user_data is False:
            return False
        else:
            return user_data["user_id"]
    except Exception:
        logger.error("Error validating Access Token")
        logger.error(traceback.format_exc())
        return False


def get_service_tokens():
    system_service_tokens, total_service_tokens, last_evaluated_key = ServiceTokens.get_records()
    current_service_tokens = ServiceTokens.records_to_dict(system_service_tokens)
    current_service_tokens_values = [current_service_token["value"] for current_service_token in current_service_tokens]

    return current_service_tokens_values


def get_user_role(user_id):
    role_id = "5e249517-92cc-4c26-a8fb-233a21b33b4c##admin"
    role = Roles.get_record_by_id(id_=role_id)
    return role.to_dict()


def is_authorized(current_path: str, user_id: str):
    role_logic_groups = get_user_role(user_id)["logic_groups"]
    allowed_paths = list()
    for role_logic_group in role_logic_groups:
        allowed_paths.extend(role_logic_group["resources"])
    if current_path in allowed_paths:
        return True
    else:
        return False


def lambda_handler(event, context):
    logger.info(event)
    logger.info("Client token: " + event["authorizationToken"])
    logger.info("Method ARN: " + event["methodArn"])

    token_prefix = event["authorizationToken"].split(" ")[0]
    token_value = event["authorizationToken"].split(" ")[1]
    """
    Validate the incoming token and produce the principal user 
    identifier associated with the token this could be accomplished 
    in a number of ways:
    1. Call out to OAuth provider
    2. Decode a JWT token inline
    3. Lookup in a self-managed DB
    """
    principal_id = None
    if token_prefix == "ServiceToken":
        principal_id = token_value
    else:
        try:
            # unverified_claims = jwt.get_unverified_claims(token_value)
            # logger.info(unverified_claims)
            # principal_id = jwt.get_unverified_claims(token_value).get("cognito:username")
            principal_id = validate_access_token(access_token=token_value)
        except Exception:
            logger.error("Error decoding token... Probably is malformed")

    """
    You can send a 401 Unauthorized response to the client by failing like so:
    raise Exception('Unauthorized')

    If the token is valid, a policy must be generated which will allow or deny access to the client,
    if access is denied, the client will receive a 403 Access Denied response,
    if access is allowed, API Gateway will proceed with the backend integration configured 
    on the method that was called
    this function must generate a policy that is associated with the recognized principal user identifier.
    Depending on your use case, you might store policies in a DB, or generate them on the fly 
    keep in mind, the policy is cached for 5 minutes by default (TTL is configurable in the authorizer)
    and will apply to subsequent calls to any method/resource in the RestApi made with the same token.
    """

    """
    The example policy below allows access to all resources in the RestApi
    """
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
        # GET CURRENT PATH
        resource_path_list = api_gateway_arn_tmp[3:]
        del resource_path_list[-1]
        resource_path = "".join(resource_path_list)
        logger.info(resource_path)

        # ADD SERVICE TOKEN VALIDATION
        current_service_tokens_values = get_service_tokens()
        if token_prefix == "ServiceToken" and token_value in current_service_tokens_values:
            logger.info(f"Allowing all methods for Service Token {token_value}")
            policy.allow_all_methods()
        else:
            logger.info(f"Token received is not a Service Token... Validating...")
            # ADD USER TOKEN VALIDATION
            if isinstance(principal_id, str) is True:
                user_authorization = is_authorized(current_path=resource_path, user_id=principal_id)
                if bool(user_authorization) is True:
                    logger.info(f"Allowing all methods for {token_value}")
                    policy.allow_all_methods()
                else:
                    logger.error(f"Denying all methods for {token_value}")
                    policy.deny_all_methods()

            # IF EVERYTHING FAILS DENY ALL METHODS
            else:
                logger.error(f"Denying all methods for {token_value}")
                policy.deny_all_methods()

    # Finally, build the policy
    auth_response = policy.build()
    auth_response["context"] = dict()

    return auth_response


if __name__ == "__main__":
    response = lambda_handler(
        event=dict(
            authorizationToken="Token eyJraWQiOiIzb2dCdmhmY3JGNVFlMnRXUW5oK2JnNjBleFFhVHdxZXZna04yVXpmcHhnPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NzU1NmQ0OS00MmI3LTRjZGUtYTY4MC1iMjI4OTZmOTk1Y2YiLCJldmVudF9pZCI6ImNiOWFkYmYwLWQxZjQtNDY3YS1iY2E3LTRjNjc0MTRjZmI4OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTI3ODkwNDUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0R0V1MwalluOCIsImV4cCI6MTU5Mjc5OTI2MywiaWF0IjoxNTkyNzk1NjYzLCJqdGkiOiIxZjhjNGM0OS1iNmYwLTRkY2MtYTdhMS1mMGE4YjczZjA4YmMiLCJjbGllbnRfaWQiOiJhbGlpNTgwNDFrNzJoaHQ4Z2I3cjJjZ24yIiwidXNlcm5hbWUiOiI2NzU1NmQ0OS00MmI3LTRjZGUtYTY4MC1iMjI4OTZmOTk1Y2YifQ.Rir8jb8tOM2vlvqTexnl6To74xeS6woVwxh-TcAa4hFem7OSO38XTlptjLHWbyCgGERj7jRkM3lXxTIxGBfIyESOIhwLkYUXhmyVs85jjxc2nqbrVm1PPgyejQPY119INijcM5I5Ctd_Sxl3iBzw_yHbEfdOJker1qlX6oZPLP9frqqVFlmqEsfe4R1Eais-ayTc9L8OCTvo7RQPUKHBvJ67APhz1ISboZNGoknxfBk-X3DcdmYGvKOezMglZCGUjvCp2F4mdCFuZLiWpN7XSRc0vj0Gi8TIHt_o_aWNSuRRzWRDEi-sOCoCKG-HxAY2iEZ3Kfeuq4Wvwel6PB3iZQ",
            methodArn="arn:aws:execute-api:us-east-1:112646120612:2qoob0tpqb/prod/GET/plans/123",
        ),
        context={},
    )
    logger.info(response)
