import os
import time
import traceback

from handlers.users_backend.models import Roles
from handlers.utils import base_response

from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def get():
    pass


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

    users = {
        "results": [
            {
                "name": "Eugenio Efrain",
                "familyName": "Breijo",
                "email": "eb+test@gmail.com",
                "phoneNumber": "+17864534511",
            },
            {
                "name": "Diago Ernesto",
                "familyName": "Estrada",
                "email": "de+test@gmail.com",
                "phoneNumber": "+17864534512",
            },
        ]
    }

    return base_response(status_code=200, dict_body=users)
