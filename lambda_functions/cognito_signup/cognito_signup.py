import os

import boto3

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    username = event['username']
    password = event['password']
    response = client.sign_up(
        ClientId=os.environ['CLIENT_ID'],
        Username=username,
        Password=password,
    )

    response2 = client.admin_confirm_sign_up(
        UserPoolId=os.environ['USER_POOL_ID'],
        Username=username
    )

    return {
        "response Signup": response,
        "response Confirm": response2
    }

