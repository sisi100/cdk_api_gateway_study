#!/usr/bin/env python3

import aws_cdk as cdk

from deployment import ApiGatewayStudyStack

app = cdk.App()
ApiGatewayStudyStack(
    app,
    "ApiGatewayStudyStack",
)

app.synth()
