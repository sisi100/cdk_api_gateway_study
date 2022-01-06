from aws_cdk import Stack
from constructs import Construct

from timeout_study_api.infrastructure import TimeoutStudyApi


class ApiGatewayStudyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        timeout_study_api = Stack(self, "TimeoutStudyApi")
        TimeoutStudyApi(timeout_study_api, "TimeoutStudyApi")
