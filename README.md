# README - Create users with dynatrace IAM

## Prerequisie :
- Python 3.6 + with module request on linux or windows
- Account IAM OAuth2 with Scope : `account-idm-read`, `account-idm-write`, `account-env-read`, `account-env-write`
- Read [doc dynatrace Oauth2](https://docs.dynatrace.com/docs/dynatrace-api/basics/dynatrace-api-authentication/account-api-authentication)

## Export Variables :
- DT_OAUTH_ACCOUNT_URN => urn 
- DT_OAUTH_CLIENT_ID => OAuth Client ID
- DT_OAUTH_CLIENT_SECRET => OAuth Client Secret
- DT_OAUTH_SSO_ENDPOINT => endpoint IAM dynatrace  

      export DT_OAUTH_ACCOUNT_URN=urn:dtaccount:12345-abcdef-6789-efghijklm
      export DT_OAUTH_CLIENT_ID=dtxx.ABCDEF
      export DT_OAUTH_CLIENT_SECRET=dtxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      export DT_OAUTH_SSO_ENDPOINT="https://sso.dynatrace.com/sso/oauth2/token"
  
![image](https://github.com/JLLormeau/IAM/assets/40337213/b4dc82c6-e01f-47ca-b8d9-f0023eddcb17)

## Sample1 :  
mapping of user to a user group

## Sample2 :  
binding of policiy with `{$BindParam}` to a user group

