# Sample2 - binding policy based on namespace
![image](https://github.com/JLLormeau/IAM/assets/40337213/a173a7a4-f5fe-4d88-9308-a4b9635704fa)

## Prerequisie :
- Python 3.6 + with module request on linux or windows
- Account IAM OAuth2 with Scope : `account-idm-write`, `account-idm-read`, `account-env-read`, `account-env-write`, `iam-policies-management`, `iam:policies:write`, `iam:policies:read`, `iam:bindings:write`, `iam:bindings:read`, `iam:effective-permissions:read`
- Read [doc dynatrace Oauth2](https://docs.dynatrace.com/docs/dynatrace-api/basics/dynatrace-api-authentication/account-api-authentication)

## Export Variables :
- DT_OAUTH_ACCOUNT_URN => urn 
- DT_OAUTH_CLIENT_ID => OAuth Client ID
- DT_OAUTH_CLIENT_SECRET => OAuth Client Secret
- DT_OAUTH_SSO_ENDPOINT => endpoint IAM dynatrace
- DT_TENANT_ID => tenant id  

      export DT_OAUTH_ACCOUNT_URN=urn:dtaccount:12345-abcdef-6789-efghijklm
      export DT_OAUTH_CLIENT_ID=dtxx.ABCDEF
      export DT_OAUTH_CLIENT_SECRET=dtxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      export DT_OAUTH_SSO_ENDPOINT="https://sso.dynatrace.com/sso/oauth2/token"
      export DT_TENANT_ID=abcd123

- Create Policy with UI and get the POLICY_ID  
![image](https://github.com/JLLormeau/IAM/assets/40337213/9fcb1758-1ed7-4a15-921a-7169e242392f)

      ALLOW storage:metrics:read WHERE storage:k8s.namespace.name = "${bindParam:namespace}"; 
      ALLOW storage:events:read WHERE storage:k8s.namespace.name = "${bindParam:namespace}"; 
      ALLOW storage:logs:read WHERE storage:k8s.namespace.name = "${bindParam:namespace}";

- Use this [script](https://raw.githubusercontent.com/JLLormeau/IAM/main/Sample2_IAM_binding_policy_with_ug/IAM_policy_by_namespace.py)  
Modify :   
  - LIST : in this script the usergroup has the name of the namespace (the user group is created if it doesn't exist)
  - POLICY_ID (create above)

- the policy is mapped with the user group  
![image](https://github.com/JLLormeau/IAM/assets/40337213/d29b66e1-92a9-44ed-a56b-b2a5e0e146a0)

- The user must also have these policies

      ALLOW storage:buckets:read;
      AppEngine - User

- Result: Access to the metrics, logs, events only of this namespace 
![image](https://github.com/JLLormeau/IAM/assets/40337213/0ad1c2ec-c9db-49ed-b55f-cac097618ef7)
