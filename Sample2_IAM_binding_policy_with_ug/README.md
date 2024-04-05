![image](https://github.com/JLLormeau/IAM/assets/40337213/0602ea5a-458d-4da9-ba0a-2cb331e4cb3e)# Sample2 - binding policy with ug

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
      export DT_TENANT_ID=abcd123
  
![image](https://github.com/JLLormeau/IAM/assets/40337213/b4dc82c6-e01f-47ca-b8d9-f0023eddcb17)

- Create Policy with UI and get the POLICY_ID

- User Group is created by the script with the policy mapping 
![image](https://github.com/JLLormeau/IAM/assets/40337213/d29b66e1-92a9-44ed-a56b-b2a5e0e146a0)

- Minimum of righ for a user
![image](https://github.com/JLLormeau/IAM/assets/40337213/f11a3d2c-25dc-4d79-a435-c925441b36b2)

- Result
  Access to the metrics, logs, events only of this namespace.
![image](https://github.com/JLLormeau/IAM/assets/40337213/0ad1c2ec-c9db-49ed-b55f-cac097618ef7)
