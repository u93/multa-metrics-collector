from aws_cdk import core
from multacdkrecipies import (
    AwsApiGatewayLambdaFanOutBE,
    AwsIotAnalyticsSimplePipeline,
    AwsLambdaLayerVenv,
    AwsSsmString,
    AwsUserServerlessBackend,
)

from src.infrastructure.configs import analytics_cold_path_config, analytics_hot_path_config, user_backend_config


class BaseStack(core.Stack):
    """
    Base Stack for MultaMetrics Backend. Will contain common configurations and resources for other Stacks
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


class UserBackendStack(core.Stack):
    """
    User Backend Stack for MultaMetrics Backend. Will contain resources necessary to handle users and auth.
    """
    def __init__(self, scope: core.Construct, id: str, config=None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        user_serverless_backend_lambdalayer = AwsLambdaLayerVenv(
            self,
            id=f"UserServerlessBE-LambdaLayer-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["USER_BACKEND_LAMBDA_LAYER"]
        )
        layer_arn = user_serverless_backend_lambdalayer.lambda_layer.layer_version_arn

        user_serverless_backend_ssm = AwsSsmString(
            self,
            id=f"UserServerlessBE-Ssm-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["USER_BACKEND_SSM"]
        )

        config["config"]["USER_BACKEND"]["authorizer_function"]["origin"]["layers"].append(layer_arn)
        config["config"]["USER_BACKEND"]["user_pool"]["triggers"]["post_confirmation"]["layers"].append(layer_arn)
        user_serverless_backend = AwsUserServerlessBackend(
            self,
            id=f"UserServerlessBE-{config['environ']}",
            prefix="multa_backend",
            environment=config["environ"],
            configuration=config["config"]["USER_BACKEND"]
        )


class UserApisBackend(core.Stack):
    """
    API Constructs to be used by MultaMetrics frontend to handle user settings, plans, roles, organizations.
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


class AnalyticsHotPathStack(core.Stack):
    """
    Hot Analytics Stack for MultaMetrics Backend. Will contain resources necessary for a rapid ingestion and
    representation of data.
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        fna_out_api = AwsApiGatewayLambdaFanOutBE(
            self,

        )


class AnalyticsColdPathStack(core.Stack):
    """
    Cold Analytics Stack for MultaMetrics Backend. Will contain resources necessary for a storage, ingestion and
    analysis and representation of timeseries data.
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


app = core.App()

for environment, configuration in user_backend_config.USER_BACKEND_CONFIGS.items():
    print(configuration)
    config = dict(environ=environment, config=configuration)
    UserBackendStack(app, id=f"UserOrganizationStack-{environment}", config=config)

# for environment, configuration in user_backend_config.USER_BACKEND_CONFIGS.items():
#     AnalyticsHotPathStack(app, id=f"AnalyticsHotPathStack-{environment}", environ=environment, configuration=configuration)
#
# for environment, configuration in user_backend_config.USER_BACKEND_CONFIGS.items():
#     AnalyticsColdPathStack(app, id=f"AnalyticsColdPathStack-{environment}", environ=environment, configuration=configuration)

app.synth()
