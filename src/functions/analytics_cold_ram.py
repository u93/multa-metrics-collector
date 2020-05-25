import os
import time


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

    return {"time": activation_time, "status": 200}


if __name__ == "__main__":
    event = {}
    lambda_handler(event=event, context={})
