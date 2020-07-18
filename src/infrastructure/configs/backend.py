USER_BACKEND_CONFIGS = {
    "dev": {
        "USER_BACKEND_LAMBDA_LAYER": {
            "identifier": "user_backend",
            "layer_name": "user_backend_venv_layer",
            "description": "Lambda Layer containing local Python's Virtual Environment.",
            "layer_runtimes": ["PYTHON_3_7"],
        },
        "USER_BACKEND_SSM": {
            "name": "user_backend_parameters",
            "description": "Parameters used by User Backend functions and resources.",
            "string_value": {"TEST": True},
        },
        "USER_BACKEND": {
            "authorizer_function": {
                "origin": {
                    "lambda_name": "user_backend_authorizer",
                    "description": "Lambda Function that will Authorize request made by API Gateway in the project.",
                    "code_path": "./src/functions/",
                    "runtime": "PYTHON_3_7",
                    "handler": "serverless_backend_authorizer.lambda_handler",
                    "layers": [],
                    "timeout": 10,
                    "environment_vars": {
                        "ENVIRONMENT": "dev",
                        "REGION": "us-east-1",
                        "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                        "USER_POOL_APP_CLIENT_ID": "4vg2pa7su7mi4e4buemab7vuvl",
                        "KEYS_URL": "https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json",
                        "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                        "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                        "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                        "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        "SERVICE_TOKENS_TABLE_NAME": "multa_backend_service_tokens_table_dev",
                    },
                    "iam_actions": ["*"],
                }
            },
            "dynamo_tables": [
                {
                    "table_name": "organization_data",
                    "partition_key": "id",
                    "sort_key": {"name": "setting_id", "type": "string"},
                    "stream": {"enabled": False,},
                    "billing_mode": "pay_per_request",
                    "global_secondary_indexes": [
                        {
                            "index_name": "organization_data_api_key",
                            "partition_key": "api_key"
                        }
                    ],
                },
                {
                    "table_name": "user_organization_mapping",
                    "partition_key": "id",
                    "stream": {"enabled": False,},
                    "billing_mode": "pay_per_request",
                },
                {
                    "table_name": "user_roles",
                    "partition_key": "id",
                    "stream": {"enabled": False,},
                    "billing_mode": "pay_per_request",
                },
                {
                    "table_name": "account_plans",
                    "partition_key": "id",
                    "stream": {"enabled": False,},
                    "billing_mode": "pay_per_request",
                },
                {
                    "table_name": "service_tokens",
                    "partition_key": "id",
                    "stream": {"enabled": False,},
                    "billing_mode": "pay_per_request",
                },
            ],
            "user_pool": {
                "pool_name": "user",
                "password_policy": {
                    "minimum_length": 8,
                    "temporary_password_duration": 1,
                    "require": {"lower_case": True, "upper_case": True, "digits": True},
                },
                "sign_up": {
                    "enabled": True,
                    "user_verification": {
                        "email": {
                            "subject": "Multa User Pool - Account Verification",
                            "body": "Your temporary code is {####}, please use it to confirm your account.",
                            "style": "",
                        },
                        "sms": {"body": "Your temporary code is {####}, please use it to confirm your account."},
                    },
                },
                "invitation": {
                    "email": {
                        "subject": "Multa User Pool - Invitation",
                        "body": "Multa - Your username is {username} and temporary password is {####}.",
                    },
                    "sms": {"body": "Multa - Your username is {username} and temporary password is {####}."},
                },
                "sign_in": {"order": ["email"]},
                "attributes": {
                    "standard": [
                        {"name": "email", "mutable": True, "required": True},
                        {"name": "given_name", "mutable": True, "required": True},
                        {"name": "family_name", "mutable": True, "required": True},
                        {"name": "phone_number", "mutable": True, "required": True},
                        {"name": "last_update_time", "mutable": True, "required": True},
                    ]
                },
                "app_client": {
                    "enabled": True,
                    "client_name": "user",
                    "generate_secret": False,
                    "auth_flows": {"custom": True, "refresh_token": True, "user_srp": True},
                },
                "identity_pool": {
                    "identity_pool_name": "user",
                    "allow_unauth_identities": True,
                    "unauth_role": {"actions": ["*"], "resources": ["*"]},
                    "auth_role": {"actions": ["*"], "resources": ["*"]},
                },
                "triggers": {
                    "post_confirmation": {
                        "lambda_name": "user_backend_post_confirmation",
                        "description": "Lambda Function that will handle Post Confirmation events.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "serverless_backend_triggers.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {
                            "ENVIRONMENT": "dev",
                            "REGION": "us-east-1",
                            "USER_POOL_ID": "us-east-1_3y2ZVLaJI",
                            "DEFAULT_SIGNUP_PLAN": "3367dfd3-4909-4117-a434-379b66e71d18##Basic",
                            "DEFAULT_SIGNUP_ROLE": "5e249517-92cc-4c26-a8fb-233a21b33b4c##admin",
                            "USERS_TABLE_NAME": "multa_backend_user_organization_mapping_table_dev",
                            "ORGANIZATIONS_TABLE_NAME": "multa_backend_organization_data_table_dev",
                            "PLANS_TABLE_NAME": "multa_backend_account_plans_table_dev",
                            "ROLES_TABLE_NAME": "multa_backend_user_roles_table_dev",
                        },
                        "iam_actions": ["*"],
                    },
                },
            },
        },
    },
    # "demo": {
    #
    # },
    # "prod": {
    #
    # }
}
