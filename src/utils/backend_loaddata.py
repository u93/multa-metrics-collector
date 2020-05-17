import os
import time


def lambda_handler(event, context):
    activation_time = round(time.time())
    print(activation_time)
    print(os.environ)
    print(event)

    # GET PLAN DATA FROM S3

    # GET PLAN DATA FROM DYNAMO

    # COMPARE PLAN DATA TO SEE IF PLAN HAS BEEN REMOVED FROM S3 COMPARED TO DYNAMO (USE IDs)

    # REMOVE FROM DYNAMO UNDESIRED PLANS

    # GO THRU ALL IN S3, IF EXIST IN DYNAMO -> UPDATE, IF NOT EXIST -> CREATE (USE IDs)

    return {"time": activation_time, "status": 200}
