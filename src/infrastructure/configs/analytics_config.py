ANALYTICS_CONFIGS = {
    "dev": {
        "ANALYTICS_FAN_OUT_LAMBDA_LAYER": {
            "identifier": "analytics_venv",
            "layer_name": "analytics_venv_layer",
            "description": "Lambda Layer containing local Python's Virtual Environment.",
            "layer_runtimes": ["PYTHON_3_7"],
        },
        "ANALYTICS_FAN_OUT_SSM": {
            "name": "analytics_parameters",
            "description": "Parameters used by Analytics Fan Out API functions and resources.",
            "string_value": {"TEST": True},
        },
        "ANALYTICS_INGESTION_ENGINE": {
            "queue": {
                "queue_name": "analytics_ingestion_queue",

            },
            "lambda_handlers": [
                {
                    "lambda_name": "analytics_metrics_ingestion_handler",
                    "description": "Lambda Function that will handle ingestion of IoT Reported metrics.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "analytics_metrics_ingestion.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                    },
                    "iam_actions": ["*"],
                },
            ],
            "iot_rule": {
                "rule_name": "analytics_ingestion_rule",
                "description": "IoT Rule for data ingestion coming from Multa Agents",
                "rule_disabled": False,
                "sql": "SELECT *, topic(3) AS serial_number FROM '$aws/things/+/shadow/update/documents'",
                "aws_iot_sql_version": "2016-03-23"
            }
        },
        "ANALYTICS_CONNECTIVITY_INGESTION_ENGINE": {
            "cloudwatch_rule": {
                "rule_name": "connectivity_collector",
                "description": "Cloudwatch Rule that will activate for Data Collection - Connectivity",
                "enabled": True,
                "schedule": "0/2 * * * ? *"
            },
            "lambda_handlers": [
                {
                    "lambda_name": "analytics_connectivity_ingestion_handler",
                    "description": "Lambda Function that will ingestion of Connectivity for Cold Metrics.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "analytics_connectivity_ingestion.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                    },
                    "iam_actions": ["*"],
                },
            ],
        },
        "ANALYTICS_INGESTION_PIPELINES": [
            {
                "name": "analytics_general_pipeline",
                "retention_periods": {
                    "datastore": 180,
                }
            },
            {
                "name": "analytics_connectivity_pipeline",
                "retention_periods": {
                    "datastore": 180,
                }
            }
        ],
        "ANALYTICS_FAN_OUT_API": {
            "functions": [
                {
                    "lambda_name": "analytics_cold_ram_handler",
                    "description": "Lambda Function that will handle RAM Analysis logic for Cold Analytics.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "analytics_cold_ram.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {"ENVIRONMENT": "dev"},
                    "iam_actions": ["*"],
                },
                {
                    "lambda_name": "analytics_cold_cpu_handler",
                    "description": "Lambda Function that will handle CPU Analysis logic for Cold Analytics.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "analytics_cold_cpu.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {"ENVIRONMENT": "dev"},
                    "iam_actions": ["*"],
                },
                {
                    "lambda_name": "analytics_cold_hdd_handler",
                    "description": "Lambda Function that will handle HDD Analysis logic for Cold Analytics.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "analytics_cold_hdd.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {"ENVIRONMENT": "dev"},
                    "iam_actions": ["*"],
                },
                {
                    "lambda_name": "analytics_cold_connectivity_handler",
                    "description": "Lambda Function that will handle Connectivity Analysis logic for Cold Analytics.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "analytics_cold_connectivity.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {"ENVIRONMENT": "dev"},
                    "iam_actions": ["*"],
                },
            ],
            "api": {
                "apigateway_name": "serverless_analytics_api",
                "apigateway_description": "Serverless Analytics Backend API for Frontend interaction.",
                "authorizer_function": {
                    "origin": {
                        "lambda_name": "serverless_analytics_authorizer",
                        "description": "Lambda Function that will Authorize request made by API Gateway in the project.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "serverless_backend_authorizer.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {"ENVIRONMENT": "dev"},
                        "iam_actions": ["*"],
                    }
                },
                "settings": {
                    "proxy": False,
                    "default_cors_options": {"allow_origins": ["*"], "options_status_code": 200},
                    "default_http_methods": ["ANY"],
                    "default_stage_options": {"metrics_enabled": True, "logging_level": "INFO"},
                    "default_handler": {
                        "lambda_name": "serverless_analytics_cold_default_handler",
                        "description": "Lambda Function that will handle defaulted requests to Serverless Analytics API.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "serverless_analytics_router_cold.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {"ENVIRONMENT": "dev"},
                        "iam_actions": ["*"],
                    },
                },
                "resource": {
                    "resource_name": "cold",
                    "methods": ["GET", "POST"],
                    "handler": {
                        "lambda_name": "serverless_analytics_router_cold_handler",
                        "description": "Lambda Function that will handle COLD requests to Serverless Analytics API.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "serverless_analytics_router_cold.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {"ENVIRONMENT": "dev"},
                        "iam_actions": ["*"],
                    },
                },
            },
        },
    },
    # "demo": {},
    # "prod": {}
}
