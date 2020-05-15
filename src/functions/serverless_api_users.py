import os
import time

from handlers.utils import base_response


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
    activation_time = round(time.time())
    print(activation_time)
    print(os.environ)
    print(event)

    users = {
        "results": [
            {
                "name": "Eugenio Efrain",
                "familyName": "Breijo",
                "email": "eb+test@gmail.com",
                "phoneNumber": "+17864534511"
            },
            {
                "name": "Diago Ernesto",
                "familyName": "Estrada",
                "email": "de+test@gmail.com",
                "phoneNumber": "+17864534512"
            }
        ]
    }

    return base_response(status_code=200, dict_body=users)