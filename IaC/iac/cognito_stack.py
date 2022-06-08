from aws_cdk import (
    NestedStack,
    aws_cognito as cognito,
)
from constructs import Construct

class CognitoStack(NestedStack):

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "CognitoStack")

        # Setup Cognito

        self.cognitoUserPool = cognito.UserPool(self, "UserPool",
                                           user_pool_name="ExampleUserPool",
                                           self_sign_up_enabled=True,
                                           sign_in_aliases=cognito.SignInAliases(
                                               username=True,
                                               email=True
                                           ),

                                           )

        self.cognitoClient = self.cognitoUserPool.add_client("ExampleClient",
                                                   auth_flows=cognito.AuthFlow(user_password=True),
                                                   user_pool_client_name="ExampleClient"
                                                   )

        self.cognitoIdentityPool = cognito.CfnIdentityPool(self, "ExampleIdentityPool",
                                                      allow_unauthenticated_identities=False,
                                                      cognito_identity_providers=[
                                                          cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                                                              client_id=self.cognitoClient.user_pool_client_id,
                                                              provider_name=f"cognito-idp.{self.region}.amazonaws.com/{self.cognitoUserPool.user_pool_id}"
                                                          )
                                                      ]
                                                      )
