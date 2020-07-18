BASE_CONFIGS = {
    "dev": {
        "BASE_CONFIG_LAMBDA_LAYER": {
            "identifier": "base_backend",
            "layer_name": "base_backend_venv_layer",
            "description": "Lambda Layer containing local Python's Virtual Environment.",
            "layer_runtimes": ["PYTHON_3_7"],
        },
        "BASE_CONFIG_SSM": {
            "name": "base_backend_parameters",
            "description": "Parameters used by Base Backend functions and resources.",
            "string_value": {"TEST": True},
        },
        "BASE_CONFIG_BUCKETS": {
            "buckets": [{"bucket_name": "backend-static-data", "versioned": False, "public_read_access": False}],
        },
        "BASE_CONFIG_FUNCTIONS": {
            "functions": [
                {
                    "lambda_name": "backend_plans_loaddata_handler",
                    "description": "Backend Function for loading static data into tables, S3 buckets and others.",
                    "code_path": "./src/utils/",
                    "runtime": "PYTHON_3_7",
                    "handler": "backend_plans_loaddata.lambda_handler",
                    "layers": [],
                    "timeout": 120,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                        "USERS_TABLE_NAME": "multa_backend_user_settings_table_dev",
                        "ORGANIZATIONS_TABLE_NAME": "multa_backend_organizations_table_dev",
                        "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                        "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        "LOG_LEVEL": "INFO",
                    },
                    "iam_actions": ["*"],
                },
                {
                    "lambda_name": "backend_roles_loaddata_handler",
                    "description": "Backend Function for loading static data into tables, S3 buckets and others.",
                    "code_path": "./src/utils/",
                    "runtime": "PYTHON_3_7",
                    "handler": "backend_roles_loaddata.lambda_handler",
                    "layers": [],
                    "timeout": 120,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                        "USERS_TABLE_NAME": "multa_backend_user_settings_table_dev",
                        "ORGANIZATIONS_TABLE_NAME": "multa_backend_organizations_table_dev",
                        "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                        "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        "LOG_LEVEL": "INFO",
                    },
                    "iam_actions": ["*"],
                },
                {
                    "lambda_name": "backend_service_token_loaddata_handler",
                    "description": "Backend Function for loading static data into tables, S3 buckets and others.",
                    "code_path": "./src/utils/",
                    "runtime": "PYTHON_3_7",
                    "handler": "backend_service_token_loaddata.lambda_handler",
                    "layers": [],
                    "timeout": 120,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                        "USERS_TABLE_NAME": "multa_backend_user_settings_table_dev",
                        "ORGANIZATIONS_TABLE_NAME": "multa_backend_organizations_table_dev",
                        "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                        "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        "LOG_LEVEL": "INFO",
                    },
                    "iam_actions": ["*"],
                },
                {
                    "lambda_name": "backend_user_migrations_handler",
                    "description": "Backend function to perform migrations in user data.",
                    "code_path": "./src/utils/",
                    "runtime": "PYTHON_3_7",
                    "handler": "backend_user_migrations.lambda_handler",
                    "layers": [],
                    "timeout": 120,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                        "USERS_TABLE_NAME": "multa_backend_user_settings_table_dev",
                        "ORGANIZATIONS_TABLE_NAME": "multa_backend_organizations_table_dev",
                        "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                        "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        "LOG_LEVEL": "INFO",
                    },
                    "iam_actions": ["*"],
                },
            ],
        },
    },
    # "demo": {
    #
    # },
    # "prod": {
    #
    # }
}
