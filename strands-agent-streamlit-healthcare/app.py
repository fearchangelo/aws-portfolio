#!/usr/bin/env python3
import os

from aws_cdk import App, Environment

from cdk.cdk_stack import CdkStack
from docker_app.config_file import Config


app = App()
CdkStack(app, Config.STACK_NAME,
    # Commented ENV --> imply account/region from the CLI's current configuration
    #env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    env=Environment(region=Config.DEPLOYMENT_REGION)
    )

app.synth()
