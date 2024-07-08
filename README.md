# README - IAM Policy

## Prerequisie :
- Account IAM OAuth2 with Scope : `account-idm-read`, `account-idm-write`, `account-env-read`, `account-env-write` ...
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

## Sample1 :  [link](/Sample1_IAM_create_user_with_managementzone_access)  
mapping of user to a user group

## Sample2 :  [link](/Sample2_IAM_binding_policy_with_ug)  
binding of policiy with `{$BindParam}` based on namespace

## Sample3 :  [link](/Sample3_IAM_binding_policy_based_on_gcp_project_id)  
binding of policiy with `{$BindParam}`  based on gcp.project.id

## Sample4 :  [link](/Sample4_IAM_with_Monaco)  
Configure user policies, user group and users with Monaco 

## Sample5: In Progress [Terraform]
