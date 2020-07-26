import traceback

from marshmallow import EXCLUDE, fields, Schema, validates, ValidationError

from settings.devices import DEVICE_AUTHORZATION_TOKEN_PREFIX
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


class RegisterApiAuthSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    authorization_token = fields.Str(required=True, data_key="authorizationToken", allow_none=False)

    @validates("authorization_token")
    def validate_token_prefix(self, authorization_token: str):
        try:
            prefix = authorization_token.split()[0]
            if prefix == DEVICE_AUTHORZATION_TOKEN_PREFIX:
                return True
        except Exception:
            logger.error(f"Error parsing Device Authorization Token... - {authorization_token}")
            logger.error(traceback.format_exc())

        raise ValidationError(f"Wrong token prefix! - {authorization_token}")

    @validates("authorization_token")
    def validate_token_value(self, authorization_token: str):
        try:
            value = authorization_token.split()[1]
            if isinstance(value, str):
                return True
        except Exception:
            logger.error(f"Error parsing Device Authorization Token... - {authorization_token}")
            logger.error(traceback.format_exc())

        raise ValidationError(f"Wrong token value! - {authorization_token}")


class RegisterApiSchema(Schema):
    thing_name = fields.Str(required=True, data_key="thingName")
    version = fields.Str(required=True, data_key="version")


class ThingAttributesSchema(Schema):
    version = fields.Str(required=True, data_key="version")
    organization_id = fields.Str(required=True, data_key="organization_id")
    creation_timestamp = fields.Str(required=True, data_key="creation_timestamp")


class RegisterThingSchema(Schema):
    thing_name = fields.Str(required=True, data_key="thing_name")
    thing_type_name = fields.Str(required=True, data_key="thing_type_name")
    thing_attributes = fields.Dict(values=fields.Nested(ThingAttributesSchema), data_key="thing_attributes", required=True)