SERVERLESS_REST_API_CONFIGS = {
    "dev": {
        "SERVERLESS_REST_API_LAMBDA_LAYER": {
            "identifier": "serverless_api",
            "layer_name": "serverless_api_parameters_venv_layer",
            "description": "Lambda Layer containing local Python's Virtual Environment.",
            "layer_runtimes": ["PYTHON_3_7"],
        },
        "SERVERLESS_REST_API_SSM": {
            "name": "serverless_api_parameters",
            "description": "Parameters used by Serverless Backend API functions and resources.",
            "string_value": {
                "TEST": True
            }
        },
        "SERVERLESS_REST_API": {
            "api": {
                "apigateway_name": "serverless_api",
                "apigateway_description": "Serverless Backend API for Frontend interaction.",
                "authorizer_function": {
                    "imported": {
                        "identifier": "serverless_api_authorizer_function",
                        "arn": "DYNAMIC"
                    }
                },
                "settings": {
                    "proxy": False,
                    "default_cors_options": {"allow_origins": ["*"], "options_status_code": 200},
                    "default_http_methods": ["GET"],
                    "default_handler": {
                        "lambda_name": "serverless_api_default_handler",
                        "description": "Lambda Function that will handle defaulted requests to Serverless API.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "serverless_api_default.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {"ENVIRONMENT": "dev"},
                        "iam_actions": ["*"]
                    },
                },
                "resource_trees": [
                    {
                        "resource_name": "users",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "handler": {
                            "lambda_name": "serverless_api_users_general_handler",
                            "description": "Lambda Function that will handle User-related requests to Serverless API.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "serverless_api_users.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {"ENVIRONMENT": "dev"},
                            "iam_actions": ["*"]
                        },
                        "child": {
                            "resource_name": "{user_id}",
                            "methods": ["GET", "POST", "PUT", "DELETE"],
                            "handler": {
                                "lambda_name": "serverless_api_users_individual_handler",
                                "description": "Lambda Function that will handle User-related requests to Serverless API.",
                                "code_path": "./src/functions/",
                                "runtime": "PYTHON_3_7",
                                "handler": "serverless_api_users.lambda_handler",
                                "layers": [],
                                "timeout": 10,
                                "environment_vars": {"ENVIRONMENT": "dev"},
                                "iam_actions": ["*"]
                            },
                            "childs": [
                                {
                                    "resource_name": "share",
                                    "methods": ["GET", "POST", "PUT", "DELETE"],
                                    "handler": {
                                        "lambda_name": "serverless_api_users_specific_handler",
                                        "description": "Lambda Function that will handle User-related requests to Serverless API.",
                                        "code_path": "./src/functions/",
                                        "runtime": "PYTHON_3_7",
                                        "handler": "serverless_api_users.lambda_handler",
                                        "layers": [],
                                        "timeout": 10,
                                        "environment_vars": {"ENVIRONMENT": "dev"},
                                        "iam_actions": ["*"]
                                    },
                                }
                            ]
                        }
                    }
                ]
            }
        },
    },
    # "demo": {},
    # "prod": {}
}