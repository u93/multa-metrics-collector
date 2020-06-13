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
                        "USER_POOL_ID": "us-east-1_DtWS0jYn8",
                        "USER_POOL_APP_CLIENT_ID": "5uv9ea0mr622lv76vpqhjcvoh",
                        "KEYS_URL": "https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json",
                        "REGION": "us-east-1"
                    },
                    "iam_actions": ["*"],
                }
            },
            "dynamo_tables": [
                {
                    "table_name": "organizations",
                    "partition_key": "id",
                    "stream": {"enabled": False,},
                    "billing_mode": "pay_per_request",
                },
                {
                    "table_name": "user_settings",
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
                "pool_name": "users",
                "password_policy": {
                    "minimum_length": 8,
                    "temporary_password_duration": 1,
                    "require": {"lower_case": True, "upper_case": True, "digits": True},
                },
                "sign_up": {
                    "enabled": True,
                    "user_verification": {
                        "email": {
                            "subject": "Multa User Pool - User Account",
                            "body": "Multa - Your username is {username} and temporary password is {####}. ",
                            "style": "",
                        },
                        "sms": {"body": "Multa - Your username is {username} and temporary password is {####}."},
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
                        {"name": "email", "mutable": False, "required": True},
                        {"name": "given_name", "mutable": False, "required": True},
                        {"name": "family_name", "mutable": False, "required": True},
                        {"name": "phone_number", "mutable": False, "required": True},
                        {"name": "last_update_time", "mutable": False, "required": True},
                    ]
                },
                "app_client": {
                    "enabled": True,
                    "client_name": "users",
                    "generate_secret": False,
                    "auth_flows": {"custom": True, "refresh_token": True, "user_srp": True},
                },
                "triggers": {
                    "post_confirmation": {
                        "lambda_name": "user_backend_post_confirmation",
                        "description": "Lambda Function that will handle Post Confirmation events.",
                        "code_path": "./src/functions/",
                        "runtime": "PYTHON_3_7",
                        "handler": "post_confirmation_trigger.lambda_handler",
                        "layers": [],
                        "timeout": 10,
                        "environment_vars": {"ENVIRONMENT": "dev"},
                        "iam_actions": ["*"],
                    }
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
