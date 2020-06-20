import os

USERS_TABLE_NAME = os.environ.get("USERS_TABLE_NAME", "multa_backend_user_organization_mapping_table_dev")
ORGANIZATIONS_TABLE_NAME = os.environ.get("ORGANIZATIONS_TABLE_NAME", "multa_backend_organization_data_table_dev")
PLANS_TABLE_NAME = os.environ.get("PLANS_TABLE_NAME", "multa_backend_account_plans_table_dev")
ROLES_TABLE_NAME = os.environ.get("ROLES_TABLE_NAME", "multa_backend_user_roles_table_dev")
SERVICE_TOKENS_TABLE_NAME = os.environ.get("SERVICE_TOKENS_TABLE_NAME", "multa_backend_service_tokens_table_dev")

COGNITO_TRIGGERS = {
    "POST_CONFIRMATION_CONFIRM_SIGNUP": "PostConfirmation_ConfirmSignUp"
}

ANALYTICS_LAMBDA_ROUTING_MAPPING = {
    "ram": "multa_backend_analytics_cold_ram_handler_dev",
    "cpu": "multa_backend_analytics_cold_cpu_handler_dev",
    "hdd": "multa_backend_analytics_cold_hdd_handler_dev",
    "connectivity": "multa_backend_analytics_cold_connectivity_handler_dev",
}

IOT_ANALYTICS_CHANNEL_0 = os.environ.get("IOT_ANALYTICS_CHANNEL_0")
IOT_ANALYTICS_CHANNEL_1 = os.environ.get("IOT_ANALYTICS_CHANNEL_1")
IOT_ANALYTICS_DATASTORE_0 = os.environ.get("IOT_ANALYTICS_DATASTORE_0")
IOT_ANALYTICS_DATASTORE_1 = os.environ.get("IOT_ANALYTICS_DATASTORE_1")

IOT_ANALYTICS_HOT_PATH_KEYS = {}

IOT_ANALYTICS_COLD_PATH_KEYS = {
    "ram_memory_total": None,
    "ram_memory_available": None,
    "ram_memory_percent": None,
    "ram_memory_used": None,
    "ram_memory_free": None,
    "ram_memory_shared": None,
    "ram_memory_buffers": None,
    "ram_memory_cached": None,
    "ram_swap_total": None,
    "ram_swap_used": None,
    "ram_swap_free": None,
    "ram_swap_percent": None,
    "ram_insights_current": None,
    "ram_insights_total": None,
    "ram_insights_percent": None,
    "ram_insights_status": None,
    "cpu_dynamic_insights_percent": None,
    "cpu_dynamic_insights_status": None,
    "disk_dynamic_current": None,
    "disk_dynamic_total": None,
    "disk_dynamic_percent": None,
    "disk_dynamic_insights_status": None,
    "disk_dynamic_io_read_count": None,
    "disk_dynamic_io_write_count": None,
    "disk_dynamic_io_read_bytes": None,
    "disk_dynamic_io_write_bytes": None,
    "disk_dynamic_io_read_time": None,
    "disk_dynamic_io_write_time": None,
    "temperature_current": None,
    "temperature_total": None,
    "temperature_insights_percent": None,
    "temperature_insights_status": None,
    "boot_time_insights_seconds_since_boot": None,
    "boot_time_insights_days_since_boot": None,
    "boot_time_insights_status": None,
}
