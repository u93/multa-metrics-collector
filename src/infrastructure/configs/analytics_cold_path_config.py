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
            "string_value": {
                "TEST": True
            }
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
                    "iam_actions": ["*"]
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
                    "iam_actions": ["*"]
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
                    "iam_actions": ["*"]
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
                    "iam_actions": ["*"]
                },
            ],
            "api": {
                "apigateway_name": "analytics_cold_fan_out_api",
                "apigateway_description": "Entry point for the ANALYTICS FAN OUT API",
                "proxy": False,
                "authorizer_function": {
                    "imported": {
                        "identifier": "analytics_cold_fan_out_api_authorizer_function",
                        "arn": "DYNAMIC"
                    }
                },
                "root_resource": {
                    "name": "analytics-cold",
                    "allowed_origins": ["*"],
                    "methods": ["GET"],
                    "handler": {
                        "lambda_name": "analytics_cold_router_handler",
                        "description": "Lambda Function that will handle Routing logic for Cold Analytics.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "analytics_router_cold.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {"ENVIRONMENT": "dev"},
                        "iam_actions": ["*"]
                    },
                }
            }
        },
    },
    # "demo": {},
    # "prod": {}
}