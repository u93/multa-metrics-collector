DEVICE_GATEWAY_CONFIGS = {
    "dev": {
        "LAMBDA_LAYER_CONFIGURATION": {
            "identifier": "device_gateway",
            "layer_name": "device_gateway_venv_layer",
            "description": "Lambda Layer containing local Python's Virtual Environment needed for Multa CVM Auth and Handler",
            "layer_runtimes": ["PYTHON_3_7"],
        },
        "SSM_CONFIGURATION": {
            "name": "device_gateway_parameters",
            "description": "Parameters used by Multa Device Gateway and other applications",
            "string_value": {
                "POLICY_NAMES": "multa_backend_policy_dev",
                "AWS_ROOT_CA": {
                    "PREFERRED": "https://www.amazontrust.com/repository/AmazonRootCA1.pem",
                    "BACKUP": "https://www.amazontrust.com/repository/AmazonRootCA3.pem",
                },
                "DEVICE_KEY": "TEST1234#",
            },
        },
        "APIGATEWAY_CONFIGURATION": {
            "api": {
                "apigateway_name": "device_gateway",
                "apigateway_description": "API Gateway used for Multa Device Agents to be associated to the AWS IoT",
                "authorizer_function": {
                    "origin": {
                        "lambda_name": "device_gateway_authorizer",
                        "description": "Authorizer Lambda function for Multa Device Agents",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "device_gateway_authorizer.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {
                            "LOG_LEVEL": "INFO",
                            "APP_CONFIG_PATH": "/multa_backend/dev/device_gateway_parameters",
                        },
                        "iam_actions": ["*"],
                    }
                },
                "settings": {
                    "proxy": False,
                    "custom_domain": {
                        "domain_name": "cvm-agent.dev.multa.io",
                        "certificate_arn": "arn:aws:acm:us-east-1:112646120612:certificate/48e19da0-71a4-417a-9247-c02ef100749c",
                    },
                    "default_cors_options": {"allow_origins": ["*"], "options_status_code": 200},
                    "default_http_methods": ["GET", "POST"],
                    "default_stage_options": {"metrics_enabled": True, "logging_level": "INFO"},
                    "default_handler": {
                        "lambda_name": "device_default_handler",
                        "description": "Handler Lambda for Multa Agents Certificate Vending Machine.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "device_gateway_handler.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {
                            "LOG_LEVEL": "INFO",
                            "APP_CONFIG_PATH": "/multa_backend/dev/device_gateway_parameters",
                            "THING_TYPE_NAME_RULE": "Multa",
                        },
                        "iam_actions": ["*"],
                    },
                },
                "resource_trees": [
                    {
                        "resource_name": "multa-agent",
                        "methods": ["POST"],
                        "handler": {
                            "lambda_name": "device_gateway_handler",
                            "description": "Handler Lambda for Multa Agents Certificate Vending Machine.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "device_gateway_handler.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {
                                "LOG_LEVEL": "INFO",
                                "APP_CONFIG_PATH": "/multa_backend/dev/device_gateway_parameters",
                                "THING_TYPE_NAME_RULE": "Multa",
                            },
                            "iam_actions": ["*"],
                        },
                    }
                ],
            }
        },
    }
}
