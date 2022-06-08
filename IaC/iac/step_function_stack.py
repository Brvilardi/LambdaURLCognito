from aws_cdk import (
    # Duration,
    NestedStack,
    aws_lambda as lambda_,
    aws_stepfunctions as stepfunctions,
    aws_stepfunctions_tasks as stepfunctions_tasks,
    Duration
)

from constructs import Construct
from .lambda_stack import LambdaStack


class StepFunctionStack(NestedStack):
    def __init__(self, scope: Construct, lambdaStack: LambdaStack) -> None:
        super().__init__(scope, "StepFunctionStack")

        # Setup Steps
        sign_up_job = stepfunctions_tasks.LambdaInvoke(
            self, "SignUpJob",
            lambda_function=lambdaStack.lambda_function_cognito_signup,
            result_path="$.lambdaResponse"
        )

        login_job = stepfunctions_tasks.LambdaInvoke(
            self, "LoginJob",
            lambda_function=lambdaStack.lambda_function_cognito_login
        )

        get_credentials_job = stepfunctions_tasks.LambdaInvoke(
            self, "GetCredentialsJob",
            lambda_function=lambdaStack.lambda_function_cognito_get_credentials,
            input_path="$.Payload",
            output_path="$.Payload"
        )

        # Define workflow states
        sign_up_job.next(login_job).next(get_credentials_job)


        definition = stepfunctions.Choice(self, "WorkflowChoise")\
            .when(stepfunctions.Condition.string_equals("$.action", "signup"), sign_up_job)\
            .when(stepfunctions.Condition.string_equals("$.action", "login"), login_job)

        self.state_machine = stepfunctions.StateMachine(self, "LambdaCognitoStateMachine",
            definition=definition,
            timeout=Duration.seconds(300)
        )


