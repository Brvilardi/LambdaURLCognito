#!/usr/bin/env python3
import os

import aws_cdk as cdk
from dotenv import load_dotenv

from iac.iac_stack import IaCStack

load_dotenv()

app = cdk.App()
IaCStack(app, "IaCStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT') or "000000000000", region=os.getenv('CDK_DEFAULT_REGION') or "us-east-1"),
    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    )

app.synth()
