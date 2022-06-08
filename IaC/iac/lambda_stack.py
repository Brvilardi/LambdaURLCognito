from aws_cdk import (
    NestedStack,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct

from .cognito_stack import CognitoStack


class LambdaStack(NestedStack):

    def __init__(self, scope: Construct, cognitoStack: CognitoStack) -> None:
        super().__init__(scope, "LambdaStack")

        # Setup Lambda Functions

        # =============== SERVER =======================
        self.lambda_function_server = lambda_.Function(self, 'Lambda Function Server',
                                                  runtime=lambda_.Runtime.PYTHON_3_9,
                                                  code=lambda_.Code.from_asset('../lambda_functions/server'),
                                                  handler='server.lambda_handler'
                                                  )
        self.lambda_function_server.add_function_url()
        # ===============================================


        # =============== SIGNUP =======================
        self.lambda_function_cognito_signup = lambda_.Function(self, 'Lambda Function Cognito Signup',
                                                               runtime=lambda_.Runtime.PYTHON_3_9,
                                                               code=lambda_.Code.from_asset(
                                                                   '../lambda_functions/cognito_signup'),
                                                               handler='cognito_signup.lambda_handler',
                                                               environment={
                                                                   'USER_POOL_ID': cognitoStack.cognitoUserPool.user_pool_id,
                                                                   'CLIENT_ID': cognitoStack.cognitoClient.user_pool_client_id
                                                               }
                                                               )

        self.lambda_function_cognito_signup.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "cognito-idp:AdminConfirmSignUp"
                ],
                resources=[
                    cognitoStack.cognitoUserPool.user_pool_arn
                ]
            )
        )
        # ===============================================


        # =============== LOGIN =======================
        self.lambda_function_cognito_login = lambda_.Function(self, 'Lambda Function Cognito Login',
                                                         runtime=lambda_.Runtime.PYTHON_3_9,
                                                         code=lambda_.Code.from_asset(
                                                             '../lambda_functions/cognito_login'),
                                                         handler='cognito_login.lambda_handler',
                                                         environment={
                                                             'USER_POOL_ID': cognitoStack.cognitoUserPool.user_pool_id,
                                                             'CLIENT_ID': cognitoStack.cognitoClient.user_pool_client_id
                                                         }
                                                         )

        # ===============================================


        # =============== GET CREDENTIALS =======================
        self.lambda_function_cognito_get_credentials = lambda_.Function(self, 'Lambda Function Cognito Get Credentials',
                                                                   runtime=lambda_.Runtime.PYTHON_3_9,
                                                                   code=lambda_.Code.from_asset(
                                                                       '../lambda_functions/cognito_get_credentials'),
                                                                   handler='cognito_get_credentials.lambda_handler',
                                                                   environment={
                                                                       'IDENTITY_POOL_ID': cognitoStack.cognitoIdentityPool.ref,
                                                                       'IDENTITY_POOL_REGION': self.region,
                                                                       'USER_POOL_ID': cognitoStack.cognitoUserPool.user_pool_id,
                                                                   }
                                                                   )

        self.lambda_function_cognito_get_credentials.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    'cognito-identity:GetCredentialsForIdentity',
                    'cognito-identity:GetId'
                ],
                resources=[
                    f"arn:aws:cognito-identity:{self.region}:{self.account}:identitypool/{cognitoStack.cognitoIdentityPool.ref}"
                ],
                effect=iam.Effect.ALLOW
            )
        )
        # ===============================================