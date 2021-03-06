import boto3
import os


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    username = event['username']
    password = event['password']
    response = client.initiate_auth(
        ClientId=os.environ['CLIENT_ID'],
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    accessToken = response['AuthenticationResult']['AccessToken']
    idToken = response['AuthenticationResult']['IdToken']
    refreshToken = response['AuthenticationResult']['RefreshToken']

    return {
        "accessToken": accessToken,
        "idToken": idToken,
        "refreshToken": refreshToken
    }

