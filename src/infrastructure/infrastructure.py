from aws_cdk import core
from multacdkrecipies import (
    AwsApiGatewayLambdaFanOutBE,
    AwsApiGatewayLambdaPipes,
    AwsIotAnalyticsSimplePipeline,
    AwsLambdaFunctionsCluster,
    AwsLambdaLayerVenv,
    AwsS3BucketsCluster,
    AwsSsmString,
    AwsUserServerlessBackend,
)

from src.infrastructure.configs import (
    analytics_cold_path_config,
    base_configs,
    serverless_rest_api_configs,
    user_backend_config,
)


class BaseStack(core.Stack):
    """
    Base Stack for MultaMetrics Backend. Will contain common configurations and resources for other Stacks
    """

    def __init__(self, scope: core.Construct, id: str, config=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._base_stack_lambdalayer = AwsLambdaLayerVenv(
            self,
            id=f"BaseStack-LambdaLayer-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["BASE_CONFIG_LAMBDA_LAYER"],
        )
        layer_arn = self._base_stack_lambdalayer.lambda_layer.layer_version_arn

        self._base_stack_backend_ssm = AwsSsmString(
            self,
            id=f"BaseStack-Ssm-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["BASE_CONFIG_SSM"],
        )

        for lambda_function in config["config"]["BASE_CONFIG_FUNCTIONS"]["functions"]:
            lambda_function["layers"].append(layer_arn)
        self._helper_functions = AwsLambdaFunctionsCluster(
            self,
            id=f"BaseBackend-Functions-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["BASE_CONFIG_FUNCTIONS"],
        )

        self._base_backend_buckets = AwsS3BucketsCluster(
            self,
            id=f"BaseBackend-Buckets-{config['environ']}",
            prefix="multa-backend",
            environment=config["environ"],
            configuration=config["config"]["BASE_CONFIG_BUCKETS"],
        )


class UserBackendStack(core.Stack):
    """
    User Backend Stack for MultaMetrics Backend. Will contain resources necessary to handle users and auth.
    """

    def __init__(self, scope: core.Construct, id: str, config=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._user_serverless_backend_lambdalayer = AwsLambdaLayerVenv(
            self,
            id=f"UserServerlessBE-LambdaLayer-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["USER_BACKEND_LAMBDA_LAYER"],
        )
        layer_arn = self._user_serverless_backend_lambdalayer.lambda_layer.layer_version_arn

        self._user_serverless_backend_ssm = AwsSsmString(
            self,
            id=f"UserServerlessBE-Ssm-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["USER_BACKEND_SSM"],
        )

        config["config"]["USER_BACKEND"]["authorizer_function"]["origin"]["layers"].append(layer_arn)
        config["config"]["USER_BACKEND"]["user_pool"]["triggers"]["post_confirmation"]["layers"].append(layer_arn)
        self._user_serverless_backend = AwsUserServerlessBackend(
            self,
            id=f"UserServerlessBE-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["USER_BACKEND"],
        )

    def lambda_authorizer_arn(self):
        return self._user_serverless_backend.authorizer_function.function_arn


class UserApisBackend(core.Stack):
    """
    API Constructs to be used by MultaMetrics frontend to handle user settings, plans, roles, organizations.
    """

    def __init__(self, scope: core.Construct, id: str, config=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._serverless_rest_api = AwsApiGatewayLambdaPipes(
            self,
            id=f"ServerlessRestApi-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["SERVERLESS_REST_API"],
        )


class AnalyticsHotPathStack(core.Stack):
    """
    Hot Analytics Stack for MultaMetrics Backend. Will contain resources necessary for a rapid ingestion and
    representation of data.
    """

    def __init__(self, scope: core.Construct, id: str, config=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


class AnalyticsColdPathStack(core.Stack):
    """
    Cold Analytics Stack for MultaMetrics Backend. Will contain resources necessary for a storage, ingestion and
    analysis and representation of timeseries data.
    """

    def __init__(self, scope: core.Construct, id: str, config=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        fan_out_api = AwsApiGatewayLambdaFanOutBE(
            self,
            id=f"AnalyticsColdPath-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["ANALYTICS_FAN_OUT_API"],
        )


app = core.App()

for environment, configuration in base_configs.BASE_CONFIGS.items():
    # print(configuration)
    config = dict(environ=environment, config=configuration)
    base_backend = BaseStack(app, id=f"BackendBaseStack-{environment}", config=config)

lambda_authorizers = dict()
for environment, configuration in user_backend_config.USER_BACKEND_CONFIGS.items():
    # print(configuration)
    config = dict(environ=environment, config=configuration)
    user_backend = UserBackendStack(app, id=f"UserOrganizationStack-{environment}", config=config)

    lambda_authorizers[environment] = user_backend.lambda_authorizer_arn()

for environment, configuration in serverless_rest_api_configs.SERVERLESS_REST_API_CONFIGS.items():
    configuration["SERVERLESS_REST_API"]["api"]["authorizer_function"]["imported"]["arn"] = lambda_authorizers[
        environment
    ]
    config = dict(environ=environment, config=configuration)
    UserApisBackend(app, id=f"UserApisBackend-{environment}", config=config)

for environment, configuration in analytics_cold_path_config.ANALYTICS_COLD_PATH_CONFIGS.items():
    config = dict(environ=environment, config=configuration)
    AnalyticsColdPathStack(app, id=f"AnalyticsColdPathStack-{environment}", config=config)


app.synth()
