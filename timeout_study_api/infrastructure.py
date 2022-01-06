import pathlib

from aws_cdk import Duration, aws_apigateway, aws_lambda
from constructs import Construct


class TimeoutStudyApi(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)

        api = aws_apigateway.RestApi(self, "Api")

        # API Gatewayが処置待ち中にlambdaがTimeoutした場合の調査
        timeout_lambda = aws_lambda.Function(
            self, "TimeoutLambda", **self.__build_lambda_param(timeout=1, sleep_time=5)
        )  # 処理中にtimeoutするlambda
        api.root.add_resource("lambda-timeout").add_method(
            **self.__build_api_method_param(timeout_lambda, 10)
        )  # lambdaのtimeout以上待ってくれるgateway

        # Lambdaの処理中にAPI Gatewayがtimeoutするときの調査
        long_processing_lambda = aws_lambda.Function(
            self, "NoTimeoutLambda", **self.__build_lambda_param(timeout=10, sleep_time=9)
        )  # 9秒寝ているlambda
        api.root.add_resource("gateway-timeout").add_method(
            **self.__build_api_method_param(long_processing_lambda)
        )  # 1秒でtimeoutするgateway

    def __build_api_method_param(self, _lambda, api_gateway_timeout=1):
        return dict(
            http_method="GET",
            integration=aws_apigateway.LambdaIntegration(_lambda, timeout=Duration.seconds(api_gateway_timeout)),
        )

    def __build_lambda_param(self, timeout=5, sleep_time=0):
        return dict(
            code=aws_lambda.Code.from_asset(str(pathlib.Path(__file__).resolve().parent.joinpath("runtime"))),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            timeout=Duration.seconds(timeout),
            environment={"SLEEP_TIME": str(sleep_time)},
        )
