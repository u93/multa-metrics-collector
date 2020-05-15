

ANALYTICS_SIMPLE_PIPELINE_CONFIGURATION = {
    "analytics_resource_name": "collector_pipe",
    "iot_rule": {
        "rule_name": "flat_metrics_collector_pipe",
        "description": "iot_rule_flat_metrics_collector_analytic_pipe",
        "rule_disabled": False,
        "sql": "SELECT *, topic(3) as serial_number FROM 'tlm/system/+/d2c'",
        "aws_iot_sql_version": "2016-03-23",
    },
}

# SSM_CONFIGURATION = {
#     "name": "cvm-config-parameters",
#     "description": "Parameters used by Multa CVM API and other applications",
#     "string_value": {
#         "POLICY_NAMES": "multa-base_multaCvmPermissions_dev",
#         "AWS_ROOT_CA": {
#             "PREFERRED": "https://www.amazontrust.com/repository/AmazonRootCA1.pem",
#             "BACKUP": "https://www.amazontrust.com/repository/AmazonRootCA3.pem",
#         },
#         "DEVICE_KEY": "TEST1234#",
#     },
# }