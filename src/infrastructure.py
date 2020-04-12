from aws_cdk import core
from multacdkrecipies import AwsIotAnalyticsSimplePipeline, AwsLambdaLayerVenv, AwsSsmString

ANALYTICS_SIMPLE_PIPELINE_CONFIGURATION = {
    "analytics_resource_name": "collector_pipe",
    "iot_rule": {
        "rule_name": "flat_metrics_collector_pipe",
        "description": "iot_rule_flat_metrics_collector_analytic_pipe",
        "rule_disabled": False,
        "sql": "SELECT *, topic(3) as serial_number FROM 'tlm/system/+/d2c'",
        "aws_iot_sql_version": "2016-03-23",
    },
}

SSM_CONFIGURATION = {
    "name": "cvm-config-parameters",
    "description": "Parameters used by Multa CVM API and other applications",
    "string_value": {
        "POLICY_NAMES": "multa-base_multaCvmPermissions_dev",
        "AWS_ROOT_CA": {
            "PREFERRED": "https://www.amazontrust.com/repository/AmazonRootCA1.pem",
            "BACKUP": "https://www.amazontrust.com/repository/AmazonRootCA3.pem",
        },
        "DEVICE_KEY": "TEST1234#",
    },
}

# class BaseStack(core.Stack):
#     def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
#         super().__init__(scope, id, **kwargs)
#         lambda_layer_local = AwsLambdaLayerVenv(
#             self, id="Layer-Venv", prefix="multa-base", environment="dev", configuration=LAMBDA_LAYER_CONFIGURATION
#         )
#         iot_policy = AwsIotPolicy(
#             self, id="Iot-Policies", prefix="multa-base", environment="dev", configuration=IOT_POLICY
#         )


class AnalyticsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # ssm_configuration = AwsSsmString(
        #     self, id="Api-Ssm", prefix="multa-cvm", environment="dev", configuration=SSM_CONFIGURATION
        # )
        flat_analytics_simple_pipeline = AwsIotAnalyticsSimplePipeline(
            self,
            id="Api-FSAP",
            prefix="multa_fsap",
            environment="dev",
            configuration=ANALYTICS_SIMPLE_PIPELINE_CONFIGURATION,
        )

        # ssm_configuration.grant_read(role=api_lambda.lambda_handler_function.role)


app = core.App()
# BaseStack(app, "BaseStack-dev")
AnalyticsStack(app, "MultaAnalyticsPipelines-dev")

app.synth()
