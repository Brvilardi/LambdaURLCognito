from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_cognito as cognito,
    aws_iam as iam,
)
from constructs import Construct

from .cognito_stack import CognitoStack
from .lambda_stack import LambdaStack


class IaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Setup Cognito
        cognitoStack = CognitoStack(self)


        # Setup Lambda Functions
        lambdaStack = LambdaStack(self, cognitoStack=cognitoStack)


        # Setup IAM Roles and Cognito Identity Pool to allow cognito users to call Lambda server function

        allowInvokeServerLambdaPolicyStatement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "lambda:InvokeFunctionUrl",
            ],
            resources=[lambdaStack.lambda_function_server.function_arn]
        )

        cognitoAuthRole = iam.Role(self, "CognitoAuthRole",
            assumed_by=iam.WebIdentityPrincipal("cognito-identity.amazonaws.com",
                    {
                        "StringEquals": {"cognito-identity.amazonaws.com:aud": f"{cognitoStack.cognitoIdentityPool.ref}"}
                    }
            )
        )

        cognitoAuthRole.add_to_policy(allowInvokeServerLambdaPolicyStatement)


        cognito.CfnIdentityPoolRoleAttachment(self, "CognitoIdentityPoolRoleAttachment",
            identity_pool_id=cognitoStack.cognitoIdentityPool.ref,
            roles={
                "authenticated": cognitoAuthRole.role_arn
            }
        )








