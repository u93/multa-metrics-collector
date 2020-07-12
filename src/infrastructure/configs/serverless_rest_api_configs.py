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
            "string_value": {"TEST": True},
        },
        "SERVERLESS_REST_API": {
            "api": {
                "apigateway_name": "serverless_api",
                "apigateway_description": "Serverless Backend API for Frontend interaction.",
                "authorizer_function": {
                    "imported": {"identifier": "serverless_api_authorizer_function", "arn": "DYNAMIC"}
                },
                "settings": {
                    "proxy": False,
                    "custom_domain": {
                        "domain_name": "multa-metrics-api.dev.multa.io",
                        "certificate_arn": "arn:aws:acm:us-east-1:112646120612:certificate/48e19da0-71a4-417a-9247-c02ef100749c",
                    },
                    "default_cors_options": {"allow_origins": ["*"], "options_status_code": 200},
                    "default_http_methods": ["GET"],
                    "default_stage_options": {"metrics_enabled": True, "logging_level": "INFO"},
                    "default_handler": {
                        "lambda_name": "serverless_api_default_handler",
                        "description": "Lambda Function that will handle defaulted requests to Serverless API.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "serverless_api_default.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {
                            "ENVIRONMENT": "dev",
                            "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                            "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                            "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                            "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                            "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        },
                        "iam_actions": ["*"],
                    },
                },
                "resource_trees": [
                    {
                        "resource_name": "current-info",
                        "methods": ["GET"],
                        "handler": {
                            "lambda_name": "serverless_api_current_info_handler",
                            "description": "Lambda Function that will handle User/Org current info requests to Serverless API.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "serverless_api_current_info.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {
                                "ENVIRONMENT": "dev",
                                "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                                "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                            },
                            "iam_actions": ["*"],
                        },
                    },
                    {
                        "resource_name": "user-invite",
                        "methods": ["POST"],
                        "handler": {
                            "lambda_name": "serverless_api_user_invite_handler",
                            "description": "Lambda Function that will handle User/Org current info requests to Serverless API.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "serverless_api_user_invite.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {
                                "ENVIRONMENT": "dev",
                                "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                                "INVITE_EMAIL_SENDER": "eebf1993@gmail.com",
                                "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                            },
                            "iam_actions": ["*"],
                        },
                    },
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
                            "environment_vars": {
                                "ENVIRONMENT": "dev",
                                "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                                "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                            },
                            "iam_actions": ["*"],
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
                                "environment_vars": {
                                    "ENVIRONMENT": "dev",
                                    "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                                    "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                    "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                    "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                    "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                                },
                                "iam_actions": ["*"],
                            },
                            # "childs": [
                            #     {
                            #         "resource_name": "share",
                            #         "methods": ["GET", "POST", "PUT", "DELETE"],
                            #         "handler": {
                            #             "lambda_name": "serverless_api_users_specific_handler",
                            #             "description": "Lambda Function that will handle User-related requests to Serverless API.",
                            #             "code_path": "./src/functions/",
                            #             "runtime": "PYTHON_3_7",
                            #             "handler": "serverless_api_users.lambda_handler",
                            #             "layers": [],
                            #             "timeout": 10,
                            #             "environment_vars": {"ENVIRONMENT": "dev"},
                            #             "iam_actions": ["*"],
                            #         },
                            #     }
                            # ],
                        },
                    },
                    {
                        "resource_name": "plans",
                        "methods": ["GET"],
                        "handler": {
                            "lambda_name": "serverless_api_plans_general_handler",
                            "description": "Lambda Function that will handle Plans-related requests to Serverless API.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "serverless_api_plans.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {
                                "ENVIRONMENT": "dev",
                                "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                            },
                            "iam_actions": ["*"],
                        },
                    },
                    {
                        "resource_name": "roles",
                        "methods": ["GET"],
                        "handler": {
                            "lambda_name": "serverless_api_roles_general_handler",
                            "description": "Lambda Function that will handle Roles-related requests to Serverless API.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "serverless_api_roles.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {
                                "ENVIRONMENT": "dev",
                                "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                            },
                            "iam_actions": ["*"],
                        },
                    },
                    {
                        "resource_name": "devices",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "handler": {
                            "lambda_name": "serverless_api_devices_handler",
                            "description": "Lambda Function that will handle Device-related requests to Serverless API.",
                            "code_path": "./src/functions/",
                            "runtime": "PYTHON_3_7",
                            "handler": "serverless_api_devices.lambda_handler",
                            "layers": [],
                            "timeout": 10,
                            "environment_vars": {
                                "ENVIRONMENT": "dev",
                                "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                                "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                            },
                            "iam_actions": ["*"],
                        },
                        "child": {
                            "resource_name": "{device_id}",
                            "methods": ["GET", "POST", "PUT", "DELETE"],
                            "handler": {
                                "lambda_name": "serverless_api_devices_individual_handler",
                                "description": "Lambda Function that will handle Device-related requests to Serverless API.",
                                "code_path": "./src/functions/",
                                "runtime": "PYTHON_3_7",
                                "handler": "serverless_api_devices_individual.lambda_handler",
                                "layers": [],
                                "timeout": 10,
                                "environment_vars": {
                                    "ENVIRONMENT": "dev",
                                    "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                                    "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                                    "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                                    "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                                    "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                                },
                                "iam_actions": ["*"],
                            },
                        },
                    },
                ],
            }
        },
    },
    # "demo": {},
    # "prod": {}
}
