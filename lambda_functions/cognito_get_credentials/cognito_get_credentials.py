import os

import boto3


def lambda_handler(event, context):
    client = boto3.client('cognito-identity')
    idToken = event['idToken']

    response1 = client.get_id(
        IdentityPoolId=f"{os.environ['IDENTITY_POOL_ID']}",
        Logins={
            f'cognito-idp.{os.environ["IDENTITY_POOL_REGION"]}.amazonaws.com/{os.environ["USER_POOL_ID"]}': idToken
        }
    )

    print("Get id response:", response1)

    response2 = client.get_credentials_for_identity(
        IdentityId=response1['IdentityId'],
        Logins={
            f'cognito-idp.{os.environ["IDENTITY_POOL_REGION"]}.amazonaws.com/{os.environ["USER_POOL_ID"]}': idToken
        }
    )

    print("Get credentials response:", response2)

    return {
        "AccessKeyId": response2["Credentials"]["AccessKeyId"],
        "SecretKey": response2["Credentials"]["SecretKey"],
        "SessionToken": response2["Credentials"]["SessionToken"]
    }