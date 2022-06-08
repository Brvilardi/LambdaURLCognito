


Prerequisites (todo)
- python 3.9.x
- aws cli (link)
- aws cdk (link) - versao 2.25.0 (build ae1cb4b)
- conta aws (link)



Step by step (TODO)

- create .env with CDK_DEFAULT_ACCOUNT and CDK_DEFAULT_REGION
- setup IaC/.venv
- run cdk bootstrap
- run cdk deploy


Test
Using Lambda Console:
- Create user 
  - LambdaCognitoSignUp (pass username and password on event)
- Login user to get idToken
  - LambdaCognitoSignIn (pass username and password on event) and grab idToken
- Get AWS Temporary Credentials
  - LambdaCognitoGetCredentials (pass idToken on event) and grab accessKeyId, secretAccessKey, sessionToken

Using Postman:
- grab credentials
- grab LambdaServer functio URL
- pass credentials on Postman and run

Result with credentials:
![img.png](docs_assets/postman_success.png)

Result without credentials:
![img_1.png](docs_assets/postman_fail.png)