# Sample3 - binding policy based on gcp.project.id for the global account
![image](https://github.com/JLLormeau/IAM/assets/40337213/e45b0dcf-a384-487e-8ebd-f4ceccf5eb69)

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
  

- Create Policy with UI and get the POLICY_ID  
![image](https://github.com/JLLormeau/IAM/assets/40337213/8c06eafc-d31f-4a3c-b5ee-580535186b82)

      ALLOW storage:metrics:read WHERE storage:gcp.project.id startsWith "${bindParam:name}";
      ALLOW storage:spans:read WHERE storage:gcp.project.id startsWith "${bindParam:name}";
      ALLOW storage:logs:read WHERE storage:gcp.project.id startsWith "${bindParam:name}";
      ALLOW storage:bizevents:read WHERE storage:gcp.project.id startsWith "${bindParam:name}";
      ALLOW storage:events:read WHERE storage:gcp.project.id startsWith "${bindParam:name}";

- Use this [script](https://raw.githubusercontent.com/JLLormeau/IAM/main/Sample3_IAM_binding_policy_based_on_gcp_project_id/IAM_policy_by_gcp_project_id.py)  
Modify :   
  - LIST_GCP_PROJECT : in this script the usergroup has the name of the gcp.project.id (the user group is created if it doesn't exist)  
  - POLICY_ID (create above)


- the policy is mapped with the user group  
![image](https://github.com/JLLormeau/IAM/assets/40337213/a585f202-19c2-47c6-8e25-0e07139c457e)

- The user must also have these policies

      ALLOW storage:buckets:read;
      AppEngine - User

- Result: Access to the metrics
![image](https://github.com/JLLormeau/IAM/assets/40337213/edc78b46-e779-4d11-9bb8-ac03cbd8bf02)

