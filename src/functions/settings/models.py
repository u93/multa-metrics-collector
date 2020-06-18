import os


COMPONENT_IDS = {
    "ORGANIZATION": "organization_info",
    "USER": "user_info",
    "JOBS": "job_info",
    "API_KEYS": "api_keys"
}

DEFAULT_PLAN = os.environ.get("DEFAULT_PLAN", "3367dfd3-4909-4117-a434-379b66e71d18##Basic")