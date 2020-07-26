import os

APP_CONFIG_PATH = os.environ.get("APP_CONFIG_PATH", "/multa_backend/dev/device_gateway_parameters")
THING_TYPE_NAME_RULE = os.environ.get("THING_TYPE_NAME_RULE", "Multa")

DEVICE_AUTHORZATION_TOKEN_PREFIX = "ApiKey"
