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

    # TODO: 1) Parse EVENT METHOD and activate METHOD functions accordingly.

    # TODO: 2) Parse QUERYSTRINGS and from METHOD function INVOKE proper Lambda

    result = {
        "results": []
    }

    return base_response(status_code=200, dict_body=result)
