import os
import re
import time
import traceback

from jose import jwk, jwt
from jose.utils import base64url_decode
import requests

from handlers.users_backend.models import Roles, ServiceTokens
from settings.authorizer import USER_POOL_APP_CLIENT_ID, KEYS_URL
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get_cognito_keys():
    logger.info(KEYS_URL)
    keys = requests.get(url=KEYS_URL)
    return keys.json()["keys"]


def validate_token(access_token: str):
    try:
        # get the kid from the headers prior to verification
        headers = jwt.get_unverified_headers(access_token)
        kid = headers["kid"]

        # search for the kid in the downloaded public keys
        cognito_keys = get_cognito_keys()
        key_index = -1

        for i in range(len(cognito_keys)):
            if kid == cognito_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            logger.error("Public key not found in jwks.json")
            return False

        # construct the public key
        public_key = jwk.construct(cognito_keys[key_index])

        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(access_token).rsplit(".", 1)

        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))

        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            logger.error("Signature verification failed")
            return False

        logger.info("Signature successfully verified")

        # since we passed the verification, we can now safely
        # use the unverified claims
        claims = jwt.get_unverified_claims(access_token)

        # additionally we can verify the token expiration
        if time.time() > claims["exp"]:
            logger.error("Token is expired")
            return False

        # and the Audience  (use claims['client_id'] if verifying an access token)
        if "aud" in claims and claims["aud"] != USER_POOL_APP_CLIENT_ID:
            logger.error("Token was not issued for this audience")
            return False

        # now we can use the claims
        logger.info(claims)
        return claims["cognito:username"]

    except Exception:
        logger.error("Error decoding Token")
        logger.error(traceback.format_exc())
        return False


def get_service_tokens():
    system_service_tokens, total_service_tokens, last_evaluated_key = ServiceTokens.get_records()
    current_service_tokens = ServiceTokens.records_to_dict(system_service_tokens)
    current_service_tokens_values = [current_service_token["value"] for current_service_token in current_service_tokens]

    return current_service_tokens_values


def get_user_role(user_id):
    role_id = "5e249517-92cc-4c26-a8fb-233a21b33b4c##admin"
    roles = Roles.get_record_by_id(id_=role_id)
    for role in roles:
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

    token_value = event["authorizationToken"].split(" ")[1]
    """
    Validate the incoming token and produce the principal user 
    identifier associated with the token this could be accomplished 
    in a number of ways:
    1. Call out to OAuth provider
    2. Decode a JWT token inline
    3. Lookup in a self-managed DB
    """
    try:
        unverified_claims = jwt.get_unverified_claims(token_value)
        logger.info(unverified_claims)
        principal_id = jwt.get_unverified_claims(token_value).get("cognito:username")
        logger.info(principal_id)
    except Exception:
        logger.error("Error decoding token... Probably is malformed")
        logger.error(traceback.format_exc())
        principal_id = None

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
        current_user_info = validate_token(access_token=token_value)
        if token_value in current_service_tokens_values:
            logger.info(f"Allowing all methods for {token_value}")
            policy.allow_all_methods()

        # ADD USER TOKEN VALIDATION
        elif isinstance(current_user_info, str) is True:
            user_authorization = is_authorized(current_path=resource_path, user_id=current_user_info)
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

    """
    policy.allowMethod(HttpVerb.GET, "/pets/*")
    """

    # Finally, build the policy
    auth_response = policy.build()

    # new! -- add additional key-value pairs associated with the authenticated principal
    # these are made available by APIGW like so: $context.authorizer.<key>
    # additional context is cached
    context = {"key": "value", "number": 1, "bool": True}  # $context.authorizer.key -> value
    # context['arr'] = ['foo'] <- this is invalid, APIGW will not accept it
    # context['obj'] = {'foo':'bar'} <- also invalid

    auth_response["context"] = context
    logger.info(logger)

    return auth_response


class HttpVerb:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    ALL = "*"


class AuthPolicy(object):
    aws_account_id = ""
    """
    The AWS account id the policy will be generated for. This is used to create the method ARNs.
    """
    principal_id = ""
    """
    The principal used for the policy, this should be a unique identifier for the end user.
    """
    version = "2012-10-17"
    """
    The policy version used for the evaluation. This should always be '2012-10-17'
    """
    path_regex = "^[/.a-zA-Z0-9-\*]+$"
    """
    The regular expression used to validate resource paths for the policy.
    """

    """
    These are the internal lists of allowed and denied methods. These are lists
    of objects and each object has 2 properties: A resource ARN and a nullable
    conditions statement.
    The build method processes these lists and generates the approriate
    statements for the final policy.
    """
    allow_methods = []
    deny_methods = []

    rest_api_id = "*"
    """
    The API Gateway API id. By default this is set to '*'
    """

    region = "*"
    """
    The region where the API is deployed. By default this is set to '*'
    """

    stage = "*"
    """
    The name of the stage used in the policy. By default this is set to '*'
    """

    def __init__(self, principal, aws_account_d):
        self.aws_account_id = aws_account_d
        self.principal_id = principal
        self.allow_methods = []
        self.deny_methods = []

    def _add_method(self, effect, verb, resource, conditions):
        """Adds a method to the internal lists of allowed or denied methods. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null."""
        if verb != "*" and not hasattr(HttpVerb, verb):
            raise NameError("Invalid HTTP verb " + verb + ". Allowed verbs in HttpVerb class")
        resource_pattern = re.compile(self.path_regex)
        if not resource_pattern.match(resource):
            raise NameError("Invalid resource path: " + resource + ". Path should match " + self.path_regex)

        if resource[:1] == "/":
            resource = resource[1:]

        resource_arn = (
            "arn:aws:execute-api:"
            + self.region
            + ":"
            + self.aws_account_id
            + ":"
            + self.rest_api_id
            + "/"
            + self.stage
            + "/"
            + verb
            + "/"
            + resource
        )

        if effect.lower() == "allow":
            self.allow_methods.append({"resourceArn": resource_arn, "conditions": conditions})
        elif effect.lower() == "deny":
            self.deny_methods.append({"resourceArn": resource_arn, "conditions": conditions})

    @staticmethod
    def _get_empty_statement(effect):
        """
        Returns an empty statement object prepopulated with the correct action and the
        desired effect.
        """
        statement = {"Action": "execute-api:Invoke", "Effect": effect[:1].upper() + effect[1:].lower(), "Resource": []}

        return statement

    def _get_statement_for_effect(self, effect, methods):
        """T
        his function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy.
        """
        statements = []

        if len(methods) > 0:
            statement = self._get_empty_statement(effect)

            for curMethod in methods:
                if curMethod["conditions"] is None or len(curMethod["conditions"]) == 0:
                    statement["Resource"].append(curMethod["resourceArn"])
                else:
                    conditional_statement = self._get_empty_statement(effect)
                    conditional_statement["Resource"].append(curMethod["resourceArn"])
                    conditional_statement["Condition"] = curMethod["conditions"]
                    statements.append(conditional_statement)

            statements.append(statement)

        return statements

    def allow_all_methods(self):
        """
        Adds a '*' allow to the policy to authorize access to all methods of an API
        """
        self._add_method("Allow", HttpVerb.ALL, "*", [])

    def deny_all_methods(self):
        """
        Adds a '*' allow to the policy to deny access to all methods of an API
        """
        self._add_method("Deny", HttpVerb.ALL, "*", [])

    def allow_method(self, verb, resource):
        """
        Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods for the policy
        """
        self._add_method("Allow", verb, resource, [])

    def deny_method(self, verb, resource):
        """
        Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods for the policy
        """
        self._add_method("Deny", verb, resource, [])

    def allow_method_with_conditions(self, verb, resource, conditions):
        """
        Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition
        """
        self._add_method("Allow", verb, resource, conditions)

    def deny_method_with_conditions(self, verb, resource, conditions):
        """
        Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition
        """
        self._add_method("Deny", verb, resource, conditions)

    def build(self):
        """Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy."""
        if (self.allow_methods is None or len(self.allow_methods) == 0) and (
            self.deny_methods is None or len(self.deny_methods) == 0
        ):
            raise NameError("No statements defined for the policy")

        policy = {"principalId": self.principal_id, "policyDocument": {"Version": self.version, "Statement": []}}

        policy["policyDocument"]["Statement"].extend(self._get_statement_for_effect("Allow", self.allow_methods))
        policy["policyDocument"]["Statement"].extend(self._get_statement_for_effect("Deny", self.deny_methods))

        return policy


if __name__ == "__main__":
    response = lambda_handler(
        event=dict(
            authorizationToken="Token eyJraWQiOiJBUTcrbDNJT2ZGZzhjSHN5dDExMlwvR3BSWEM4VHV4SUtiK1pqSGd2MFpmcz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhNDE5ZGRjYy1jYjU3LTQ4ODctOGQyNC04MTZlMzY0YjNjOTIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9EdFdTMGpZbjgiLCJjb2duaXRvOnVzZXJuYW1lIjoiYTQxOWRkY2MtY2I1Ny00ODg3LThkMjQtODE2ZTM2NGIzYzkyIiwiZ2l2ZW5fbmFtZSI6IkV1Z2VuaW8iLCJhdWQiOiI1dXY5ZWEwbXI2MjJsdjc2dnBxaGpjdm9oIiwiZXZlbnRfaWQiOiIxMTU2Nzc3MC1iNWQxLTQwMGQtODQ3MC04MDA4YThkMDU4ZDkiLCJ1cGRhdGVkX2F0IjoxNTkwMjY2NjQ3NjQ2LCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTU5MTU4NjcxOCwicGhvbmVfbnVtYmVyIjoiKzE3ODY2NzU4MDU0IiwiZXhwIjoxNTkxNTkwMzE5LCJpYXQiOjE1OTE1ODY3MTksImZhbWlseV9uYW1lIjoiQnJlaWpvIiwiZW1haWwiOiJlZWJmMTk5M0BnbWFpbC5jb20ifQ.WtvoyAK5tbr-ACYs7VZI1GVN7775wmY_wVoc8US6NQfHmQXADhc5M3xUk6fEuZmKXySZifAWsCiBn-gBziC4rw0aKDzAi0icAXAJMnDAS8sxG1pJSjQS6S2fZyj4EnYkhrGrfeaFmj1UuivI6z3pDXZ_SkV67gbRrC3-1T9d7JWb33l7GinlIms7yVguIcyaYnGMGDmquSd0nEhWSu3REMzY38PigzOa-hJiUYh5VEfTv4BqWxfsLpdc0gg-AdoT6kjh_VOr5jFRP4txkEb2T6XelbWwMgvCW6HOX8EGDDvYqXslajN0HhoBc0tn60ANCmqA_sNZ78AymMaIyOxKFg",
            methodArn="arn:aws:execute-api:us-east-1:112646120612:2qoob0tpqb/prod/GET/plans/123",
        ),
        context={},
    )
    logger.info(response)
