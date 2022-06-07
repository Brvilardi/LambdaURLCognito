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


        lambda_function_server = lambda_.Function(self, 'Lambda Function Server',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/server'),
            handler='server.lambda_handler'
        )
        lambda_function_server.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)

        lambda_function_cognito_login = lambda_.Function(self, 'Lambda Function Cognito Login',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/cognito_login'),
            handler='cognito_login.lambda_handler',
            environment={
                'USER_POOL_ID': cognitoUserPool.user_pool_id,
                'CLIENT_ID': cognitoClient.user_pool_client_id
            }
        )
        lambda_function_cognito_login.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)


        lambda_function_cognito_signup = lambda_.Function(self, 'Lambda Function Cognito Signup',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/cognito_signup'),
            handler='cognito_signup.lambda_handler',
            environment={
                'USER_POOL_ID': cognitoUserPool.user_pool_id,
                'CLIENT_ID': cognitoClient.user_pool_client_id
            }
        )
        lambda_function_cognito_signup.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)

        lambda_function_cognito_signup.role.attach_inline_policy(policy=iam.Policy(self, "LambdaFunctionCognitoSignupPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "cognito-idp:AdminConfirmSignUp"
                    ],
                    resources=[
                        cognitoUserPool.user_pool_arn
                    ],
                    effect=iam.Effect.ALLOW
                )
            ]
        ))








