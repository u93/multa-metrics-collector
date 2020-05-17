ANALYTICS_COLD_PATH_CONFIGS = {
    "dev": {
        "ANALYTICS_FAN_OUT_LAMBDA_LAYER": {
            "identifier": "analytics_fan_out_cold",
            "layer_name": "analytics_fan_out_cold_parameters_venv_layer",
            "description": "Lambda Layer containing local Python's Virtual Environment.",
            "layer_runtimes": ["PYTHON_3_7"],
        },
        "ANALYTICS_FAN_OUT_SSM": {
            "name": "analytics_fan_out_cold_parameters",
            "description": "Parameters used by Analytics Fan Out API functions and resources.",
            "string_value": {"TEST": True},
        },
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
                        "handler": "authorizer.lambda_handler",
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
                    "default_stage_options": {
                        "metrics_enabled": True,
                        "logging_level": "INFO"
                    },
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
                }
            }
        },
    },
    # "demo": {},
    # "prod": {}
}
