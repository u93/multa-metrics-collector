from marshmallow import Schema, fields, validates, ValidationError


class RegisterApiSchema(Schema):
    thing_name = fields.Str(required=True, data_key="thingName")
    version = fields.Str(required=True, data_key="version")
    api_key = fields.Str(required=True, data_key="apiKey")


class ThingAttributesSchema(Schema):
    version = fields.Str(required=True, data_key="version")
    api_key = fields.Str(required=True, data_key="api_key")
    creation_timestamp = fields.Int(required=True, data_key="creation_timestamp")


class RegisterThingSchema(Schema):
    thing_name = fields.Str(required=True, data_key="thing_name")
    thing_type_name = fields.Str(required=True, data_key="thing_type_name")
    attribute_payload = fields.Dict(required=True, keys=fields.String(), values=fields.Nested(ThingAttributesSchema))

    # @validates("thing_type_name")
    # def thing_type_exists(self, value):
    #     # TODO: AT INIT, THE DEFAULT THING TYPES MUST BE CREATED OR LATER UPDATED BY CLI COMMAND
    #     if value not in thing_types:
    #         raise ValidationError("Thing type does not exists!")