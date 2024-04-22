# README - Configure user policies, user group and users with Monaco

## Prerequisie :
- Monacov2 https://docs.dynatrace.com/docs/manage/configuration-as-code/monaco/installation
- Monaco Accountconfiguration scope https://docs.dynatrace.com/docs/shortlink/configuration-as-code-supported-configuration#account-management-permissions

	  account-idm-read
	  account-idm-write
	  account-env-read
	  account-env-write
	  iam-policies-management
	  iam:policies:write
	  iam:policies:read
	  iam:bindings:write
	  iam:bindings:read

- (optional) Monaco Tenant configuration scope https://docs.dynatrace.com/docs/manage/configuration-as-code/monaco/guides/create-oauth-client

	  app-engine:apps:run  
	  settings:objects:read
	  settings:objects:write
	  settings:schemas:read
	  automation:workflows:read
	  automation:workflows:write
	  automation:calendars:read
	  automation:calendars:write
	  automation:rules:read
	  automation:rules:write
	  automation:workflows:admin (you need to create a custom policy granting that scope, bind a group to it, and assign your user to that group in Account Management before creating the OAuth client. For detailed information on managing policies)
	  storage:bucket-definitions:read
	  storage:bucket-definitions:write
  
## Export Variables :

- DT_ACCOUNT_ID => 12345-abcdef-6789-efghijklm (from account urn = urn:dtaccount:12345-abcdef-6789-efghijklm)
- DT_OAUTH_CLIENT_ID => OAuth Client ID
- DT_OAUTH_CLIENT_SECRET => OAuth Client Secret
- DT_OAUTH_SSO_ENDPOINT => endpoint IAM dynatrace  

      export DT_ACCOUNT_ID=12345-abcdef-6789-efghijklm
      export DT_OAUTH_CLIENT_ID=dtxx.ABCDEF
      export DT_OAUTH_CLIENT_SECRET=dtxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      export DT_OAUTH_SSO_ENDPOINT="https://sso.dynatrace.com/sso/oauth2/token"

## Download (backup)
- with manifest
 
	  monaco account download --manifest manifest.yaml --account my-account --verbose --project backup_iam_policies

- with manifest
  
	  monaco account download --uuid %DT_ACCOUNT_ID% --oauth-client-id=DT_OAUTH_CLIENT_ID_MONACO --oauth-client-secret=DT_OAUTH_CLIENT_SECRET_MONACO

## Deploy account
- monaco cmd
  
	  monaco account deploy --manifest manifest.yaml --account my-account --verbose --project team_dev

## Delete
- monaco cmd
    
           monaco account delete --manifest manifest.yaml --file delete.yaml --account my-account

## Doc
Manifest with Account_ID = https://docs.dynatrace.com/docs/manage/configuration-as-code/monaco/configuration/account-configuration

Download with account = https://docs.dynatrace.com/docs/manage/configuration-as-code/monaco/reference/commands#download-account

Other samples = https://docs.dynatrace.com/docs/shortlink/configuration-as-code-account-configuration#example-account-management-resources-representation
