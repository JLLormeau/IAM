# README - Create users with dynatrace IAM

Prerequisie :
- Python 3.6 +
- module request
- linux or windows

Variables 
- DT_OAUTH_ACCOUNT_URN => urn 
- DT_OAUTH_CLIENT_ID => OAuth Client ID
- DT_OAUTH_CLIENT_SECRET => OAuth Client Secret
- DT_OAUTH_SSO_ENDPOINT => endpoint IAM dynatrace  
with Scope :  account-idm-write account-idm-read  
Examples :

      export DT_OAUTH_ACCOUNT_URN=urn:dtaccount:12345-abcdef-6789-efghijklm
      export DT_OAUTH_CLIENT_ID=dt0s02.ABCDEF
      export DT_OAUTH_CLIENT_SECRET=dt0s02.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      export DT_OAUTH_SSO_ENDPOINT="https://sso.dynatrace.com/sso/oauth2/token"
  
For each new project we need 2 variables : 
- NAMESPACE = name of project
- EMAILS = list of @email (separator ";") to attach to the project NAMESPACE  
Examples :

      export NAMESPACE="prd.myproject"
      export EMAILS=email1@domain.com;email2@domain.com;email3@domain.com
