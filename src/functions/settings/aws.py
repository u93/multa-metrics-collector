import os

USERS_TABLE_NAME = (os.environ.get("USERS_TABLE_NAME"),)
ORGANIZATIONS_TABLE_NAME = os.environ.get("ORGANIZATIONS_TABLE_NAME")
PLANS_TABLE_NAME = os.environ.get("PLANS_TABLE_NAME", "multa_backend_account_plans_table_dev")
ROLES_TABLE_NAME = os.environ.get("ROLES_TABLE_NAME")
SERVICE_TOKENS_TABLE_NAME = os.environ.get("SERVICE_TOKENS_TABLE_NAME", "multa_backend_service_tokens_table_dev")

ANALYTICS_LAMBDA_ROUTING_MAPPING = {
    "ram": "multa_backend_analytics_cold_ram_handler_dev",
    "cpu": "multa_backend_analytics_cold_cpu_handler_dev",
    "hdd": "multa_backend_analytics_cold_hdd_handler_dev",
    "connectivity": "multa_backend_analytics_cold_connectivity_handler_dev",
}
