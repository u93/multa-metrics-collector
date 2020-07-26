import os


COMPONENT_IDS = {"ORGANIZATION": "organization_info", "USER": "user_info", "JOBS": "job_info", "DEVICE": "device"}

DEFAULT_SIGNUP_PLAN = os.environ.get("DEFAULT_SIGNUP_PLAN", "3367dfd3-4909-4117-a434-379b66e71d18##Basic")
DEFAULT_SIGNUP_ROLE = os.environ.get("DEFAULT_SIGNUP_ROLE", "5e249517-92cc-4c26-a8fb-233a21b33b4c##admin")

GLOBAL_INDEXES = {
    "API_KEYS_INDEX": os.environ.get("API_KEYS_INDEX", "organization_data_api_key"),
    "ELEMENT_ID_INDEX": os.environ.get("ELEMENT_ID_INDEX", "organization_data_element_id")
}
