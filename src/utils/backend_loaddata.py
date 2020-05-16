import os
import time


def lambda_handler(event, context):
    activation_time = round(time.time())
    print(activation_time)
    print(os.environ)
    print(event)

    return {"time": activation_time, "status": 200}
