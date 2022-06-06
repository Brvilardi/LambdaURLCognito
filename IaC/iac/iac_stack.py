from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
)
from constructs import Construct

class IaCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        lambda_function_server = lambda_.Function(self, 'Lambda Function Server',
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset('../lambda_functions/server'),
            handler='server.lambda_handler'
        )

        lambda_function_server.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)



