from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    aws_cognito as cognito,
    aws_iam as iam,
)
from constructs import Construct

class IaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Setup Cognito

        cognitoUserPool = cognito.UserPool(self, "UserPool",
            user_pool_name="ExampleUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                username=True,
                email=True
            ),

        )

        cognitoClient = cognitoUserPool.add_client("ExampleClient",
           auth_flows=cognito.AuthFlow(user_password=True),
           user_pool_client_name="ExampleClient"
        )

        cognitoIdentityPool = cognito.CfnIdentityPool(self, "ExampleIdentityPool",
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=cognitoClient.user_pool_client_id,
                    provider_name=f"cognito-idp.{self.region}.amazonaws.com/{cognitoUserPool.user_pool_id}"
                )
            ]
        )

        # Setup Lambda Functions

        lambda_function_server = lambda_.Function(self, 'Lambda Function Server',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/server'),
            handler='server.lambda_handler'
        )
        lambda_function_server.add_function_url()

        lambda_function_cognito_login = lambda_.Function(self, 'Lambda Function Cognito Login',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/cognito_login'),
            handler='cognito_login.lambda_handler',
            environment={
                'USER_POOL_ID': cognitoUserPool.user_pool_id,
                'CLIENT_ID': cognitoClient.user_pool_client_id
            }
        )


        lambda_function_cognito_signup = lambda_.Function(self, 'Lambda Function Cognito Signup',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/cognito_signup'),
            handler='cognito_signup.lambda_handler',
            environment={
                'USER_POOL_ID': cognitoUserPool.user_pool_id,
                'CLIENT_ID': cognitoClient.user_pool_client_id
            }
        )

        lambda_function_cognito_signup.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "cognito-idp:AdminConfirmSignUp"
                ],
                resources=[
                    cognitoUserPool.user_pool_arn
                ]
            )
        )

        lambda_function_cognito_get_credentials = lambda_.Function(self, 'Lambda Function Cognito Get Credentials',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/cognito_get_credentials'),
            handler='cognito_get_credentials.lambda_handler',
            environment={
                'IDENTITY_POOL_ID': cognitoIdentityPool.ref,
                'IDENTITY_POOL_REGION': self.region,
                'USER_POOL_ID': cognitoUserPool.user_pool_id,
            }
        )



        lambda_function_cognito_get_credentials.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    'cognito-identity:GetCredentialsForIdentity',
                    'cognito-identity:GetId'
                    ],
                resources=[
                    f"arn:aws:cognito-identity:{self.region}:{self.account}:identitypool/{cognitoIdentityPool.ref}"
                ],
                effect=iam.Effect.ALLOW
            )
        )


        # Setup IAM Roles to allow Lambda Functions to be called by Cognito

        allowInvokeServerLambdaPolicyStatement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "lambda:InvokeFunctionUrl",
            ],
            resources=[lambda_function_server.function_arn]
        )


        cognitoAuthRole = iam.Role(self, "CognitoAuthRole",
            assumed_by=iam.WebIdentityPrincipal("cognito-identity.amazonaws.com",
                    {
                        "StringEquals": {"cognito-identity.amazonaws.com:aud": f"{cognitoIdentityPool.ref}"}
                    }
            )
        )

        cognitoAuthRole.add_to_policy(allowInvokeServerLambdaPolicyStatement)


        cognito.CfnIdentityPoolRoleAttachment(self, "CognitoIdentityPoolRoleAttachment",
            identity_pool_id=cognitoIdentityPool.ref,
            roles={
                "authenticated": cognitoAuthRole.role_arn
            }
        )








