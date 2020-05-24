import os

USERS_TABLE_NAME = (os.environ.get("USERS_TABLE_NAME"),)
ORGANIZATIONS_TABLE_NAME = os.environ.get("ORGANIZATIONS_TABLE_NAME")
PLANS_TABLE_NAME = os.environ.get("PLANS_TABLE_NAME", "multa_backend_account_plans_table_dev")
ROLES_TABLE_NAME = os.environ.get("ROLES_TABLE_NAME")
SERVICE_TOKENS_TABLE_NAME = os.environ.get("SERVICE_TOKENS_TABLE_NAME", "multa_backend_service_tokens_table_dev")
