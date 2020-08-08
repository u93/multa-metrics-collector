import traceback

import boto3

from handlers.common import Sts
from settings.aws import (
    FRONTEND_BASE_DOMAIN,
    INVITE_EMAIL_BODY_HTML,
    INVITE_EMAIL_CHARSET,
    INVITE_EMAIL_SENDER,
    INVITE_EMAIL_SUBJECT,
)
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def generate_invite_url(email_address: str, organization_name: str, organization_id: str, role: str) -> str:
    invite_link = f"{FRONTEND_BASE_DOMAIN}/invite?emailAddress={email_address}&organizationId={organization_id}&organizationName={organization_name}&role={role}"
    return invite_link


class SesHandler(Sts):
    def __init__(self):
        Sts.__init__(self)
        self.ses_client = boto3.client("ses")

    def send_invite_email(self, recipient: str, invite_url: str) -> bool:
        try:
            body = INVITE_EMAIL_BODY_HTML.format(invite_url=invite_url)
            response = self.ses_client.send_email(
                Destination={"ToAddresses": [recipient,],},
                Message={
                    "Body": {
                        "Html": {"Charset": INVITE_EMAIL_CHARSET, "Data": body,},
                        "Text": {"Charset": INVITE_EMAIL_CHARSET, "Data": body,},
                    },
                    "Subject": {"Charset": INVITE_EMAIL_CHARSET, "Data": INVITE_EMAIL_SUBJECT,},
                },
                Source=INVITE_EMAIL_SENDER,
            )
        # Display an error if something goes wrong.
        except Exception:
            logger.error(f"Error sending email to {recipient}")
            logger.error(traceback.format_exc())
            return False

        else:
            logger.info(f"Email sent! Message ID: {response['MessageId']}")
            logger.info(response)
            return True


if __name__ == "__main__":
    recipient = "eugeniobreijo2016@gmail.com"
    org_id = "123"
    invite_url_ = generate_invite_url(email_address=recipient, organization_name=org_id)
    cognito_handler = SesHandler()
    result = cognito_handler.send_invite_email(recipient=recipient, invite_url=invite_url_)
    logger.info(result)
