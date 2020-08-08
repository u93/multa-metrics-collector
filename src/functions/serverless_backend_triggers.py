import traceback

from handlers.backend.models import Organizations, Users, UserOrganizationRelation
from settings.aws import COGNITO_TRIGGERS, COGNITO_CONFIRMSIGNUP_USES
from settings.logs import Logger
from settings.models import DEFAULT_SIGNUP_PLAN, DEFAULT_SIGNUP_ROLE

logs_handler = Logger()
logger = logs_handler.get_logger()


def post_confirmation_signup(event: dict):
    cognito_username = event["userName"]
    try:
        user_attributes = event["request"]["userAttributes"]
        cognito_user_email = user_attributes["email"]

        client_metadata = event["request"]["clientMetadata"]
        organization_name = client_metadata.get("organization_name")
        user_role = client_metadata.get("role", DEFAULT_SIGNUP_ROLE)

        # Validates payload for the trigger activation.
        if organization_name is None:
            logger.error(f"Organization name not found for user - {cognito_username}")
            return False

        # Validates multiple trigger activations.
        user_relation = UserOrganizationRelation.get_record_by_id(id_=cognito_username)
        if user_relation is True:
            logger.error(f"User/Organization relation found for user - {cognito_username}")
            return False

        # Create Organization resource.
        organization = Organizations.create(name=organization_name, plan=DEFAULT_SIGNUP_PLAN, owner=cognito_username)

        # Create User/Organization mapping resource.
        user_organization_mapping = UserOrganizationRelation.create(
            user_id=cognito_username, organization_id=organization.id
        )

        # Create User Settings resource.
        user_settings = Users.create(organization_id=organization.id, user_id=cognito_username, role=user_role)
    except Exception:
        logger.error(f"Error creating organization/relations/user - {cognito_username}")
        logger.error(traceback.format_exc())
        return False
    else:
        return True


def post_confirmation_user_invite(event: dict):
    pass


def lambda_handler(event, context):
    logger.info(event)
    cognito_event = event["triggerSource"]

    # Validates Cognito Trigger event.
    if cognito_event == COGNITO_TRIGGERS["POST_CONFIRMATION_CONFIRM_SIGNUP"]:
        if event["request"]["clientMetadata"].get("usage") == COGNITO_CONFIRMSIGNUP_USES["signUp"]:
            post_confirmation_result = post_confirmation_signup(event=event)
        elif event["request"]["clientMetadata"].get("usage") == COGNITO_CONFIRMSIGNUP_USES["userInvite"]:
            post_confirmation_result = post_confirmation_user_invite(event=event)
        else:
            logger.error("Post Confirmation event not recognized...")
            raise Exception

        logger.info(post_confirmation_result)

    return event


if __name__ == "__main__":
    lambda_event = {
        "version": "1",
        "region": "us-east-1",
        "userPoolId": "us-east-1_DtWS0jYn8",
        "userName": "9aaa508c-511d-4a09-91e2-1a44e1804d57",
        "callerContext": {"awsSdkVersion": "aws-sdk-unknown-unknown", "clientId": "alii58041k72hht8gb7r2cgn2"},
        "triggerSource": "PostConfirmation_ConfirmSignUp",
        "request": {
            "userAttributes": {
                "sub": "9aaa508c-511d-4a09-91e2-1a44e1804d57",
                "cognito:email_alias": "eebf1993@gmail.com",
                "cognito:user_status": "CONFIRMED",
                "email_verified": "true",
                "updated_at": "1592454703768",
                "phone_number_verified": "false",
                "phone_number": "+17866758054",
                "given_name": "Eugenio",
                "family_name": "Breijo",
                "email": "eebf1993@gmail.com",
            },
            "clientMetadata": {"organization_name": "Eugenio's Dev Org", "usage": "signUp"},
        },
        "response": {},
    }
    result = lambda_handler(event=lambda_event, context={})
