import os

REGION = os.environ.get("REGION")
USER_POOL_ID = os.environ.get("USER_POOL_ID")
USER_POOL_APP_CLIENT_ID = os.environ.get("USER_POOL_APP_CLIENT_ID")
KEYS_URL_RAW = os.environ.get("KEYS_URL")
if KEYS_URL_RAW is not None:
    KEYS_URL = KEYS_URL_RAW.format(region=REGION, user_pool_id=USER_POOL_ID)
    print(KEYS_URL)
