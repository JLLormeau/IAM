# README - Create users with dynatrace IAM

## Prerequisie :
- Python 3.6 + with module request on linux or windows
- Account IAM OAuth2 with Scope : `account-idm-write` `account-idm-read`
- Read [doc dynatrace](https://docs.dynatrace.com/docs/dynatrace-api/basics/dynatrace-api-authentication/account-api-authentication)

## Export Variables 
- DT_OAUTH_ACCOUNT_URN => urn 
- DT_OAUTH_CLIENT_ID => OAuth Client ID
- DT_OAUTH_CLIENT_SECRET => OAuth Client Secret
- DT_OAUTH_SSO_ENDPOINT => endpoint IAM dynatrace  

      export DT_OAUTH_ACCOUNT_URN=urn:dtaccount:12345-abcdef-6789-efghijklm
      export DT_OAUTH_CLIENT_ID=dtxx.ABCDEF
      export DT_OAUTH_CLIENT_SECRET=dtxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      export DT_OAUTH_SSO_ENDPOINT="https://sso.dynatrace.com/sso/oauth2/token"
  

- NAMESPACE = name of project (prerequisite : must be created as a Management Zone on tenant side)
- EMAILS = list of @email (separator ",") to attach to the project NAMESPACE  

      export NAMESPACE="prd.myproject"
      export EMAILS=email1@domain.com,email2@domain.com,email3@domain.com

## Run script 
1- on new project to create users based on email list 
2- add new user on a specific project 

      python create_user_access_for_dynatrace.py

![image](https://github.com/JLLormeau/IAM/assets/40337213/33531bb0-5537-49cb-a6c5-c9267b700df0)

The user will receive this email to access to the dynatrace tenant
![image](https://github.com/JLLormeau/IAM/assets/40337213/f11c3948-ba3b-4702-a745-62469b3d9d1b)

By default, the user has these permission on each project (Management Zone): 
![image](https://github.com/JLLormeau/IAM/assets/40337213/844260a9-89d5-4a68-953a-4a324a367741)

Access on Service view
![image](https://github.com/JLLormeau/IAM/assets/40337213/93ffa6a4-ef88-424d-b750-4e0cd7ef42d2)


