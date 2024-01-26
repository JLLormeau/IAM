#JLL
import json
import requests
import os
import urllib3
import time
#import re
#from json import JSONEncoder
#import csv
import sys

##################################
### Environment variables
##################################
Account_Urn=os.getenv('DT_OAUTH_ACCOUNT_URN') #OAuth Account URN. OAuth variables are required when integrating with OAuth.
AccountUiid=Account_Urn.split(":")[2]
Client_ID=os.getenv('DT_OAUTH_CLIENT_ID') #ID	OAuth Client ID.
Client_Secret=os.getenv('DT_OAUTH_CLIENT_SECRET') #OAuth Client Secret
SSO_Endpoint=os.getenv('DT_OAUTH_SSO_ENDPOINT') #OAuth SSO endpoint with scope : account-idm-write account-idm-read
prefix_mz='gke - '
prefix_mz=''

#####projects variables
Email=list(os.getenv('EMAILS').split(","))#EMAILS=email1@domain.com,email2@domain.com,email3@domain.com
Management_Zone=prefix_mz+os.getenv('NAMESPACE')


##################################
## Variables
##################################
    
API_ACCOUNT='https://api.dynatrace.com/iam/v1/accounts/'
API_ENV='https://api.dynatrace.com/env/v1/accounts/'
PERMISSION_LIST=['tenant-viewer', 'tenant-logviewer', 'tenant-replay-sessions-with-masking']
wait=2

MZ_DIC={}
ENV_DIC={}
GROUPS_DIC={}
USERS_DIC={}

#disable warning
urllib3.disable_warnings()


##################################
## Generic Dynatrace API
##################################

# generic function GET to call API with a given uri
def queryDynatraceAPI(uri,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.get(uri,headers=head,verify=False)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function POST to call API with a given uri
def postDynatraceAPI(uri,payload,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.post(uri,headers=head,verify=False, json=payload)
    #print(response.text)
    # For  API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            try:
                jsonContent = json.loads(response.text)
            except:
                jsonContent = response.text
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function PUT to call API with a given uri
def putDynatraceAPI(uri, payload,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.put(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
        jsonContent='success'
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        #jsonContent = None
        raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

##################################
## IAM token
##################################
def iam_token():

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #scope='account-idm-write account-idm-read account-env-read account-env-write iam-policies-management iam:policies:write iam:policies:read iam:bindings:write iam:bindings:read iam:effective-permissions:read'
    scope='account-idm-write account-idm-read'
    r = requests.post(SSO_Endpoint+'?grant_type=client_credentials&client_id='+Client_ID+'&client_secret='+Client_Secret+'&resource='+Account_Urn+'&scope='+scope,headers=headers)
    #print(r.json())
    return(r.json()['access_token'])


##################################
## list of ENV
##################################
def list_env(CLIENT_ID,TOKEN):

    uri=API_ENV+CLIENT_ID+'/environments'

    datastore = queryDynatraceAPI(uri,TOKEN)
    #print(datastore)
    if datastore != []:
        for env in datastore['tenantResources']:
            ENV_DIC[env['name']]=env['id']
        for mz in datastore['managementZoneResources']:
            MZ_DIC[mz['parent']+':'+mz['id']]=mz['name']
        
    return ()


##################################
## list of GROUPS
##################################
def list_groups(CLIENT_ID,TOKEN):

    uri=API_ACCOUNT+CLIENT_ID+'/groups'

    datastore = queryDynatraceAPI(uri,TOKEN)
    #print(datastore)
    if datastore != []:
        for group in datastore['items']:
            GROUPS_DIC[group['name']]=group['uuid']
        
    return ()

##################################
## Create User GROUP
##################################
def create_group(CLIENT_ID,TOKEN,ugname):

    payload=[{
            "name": ugname,
            "description": "created by pipeline",
            "owner": "LOCAL"
            }]

    uri=API_ACCOUNT+CLIENT_ID+'/groups'
    result = postDynatraceAPI(uri,payload,TOKEN)

    print(' => create user group: '+ugname)
        
    return (result)

##################################
## Mapp MZ with User GROUP
##################################
def map_mz_ug(CLIENT_ID,TOKEN,ugid,payload):

    uri=API_ACCOUNT+CLIENT_ID+'/groups/'+ugid+'/permissions'
    result = postDynatraceAPI(uri,payload,TOKEN)

    print(' => mapp mz: '+Management_Zone+' to user group '+ugid)
        
    return (result)

##################################
## list of USERS
##################################
def list_users(CLIENT_ID,TOKEN):

    uri=API_ACCOUNT+CLIENT_ID+'/users'

    datastore = queryDynatraceAPI(uri,TOKEN)
    #print(datastore)
    if datastore != []:
        for user in datastore['items']:
            if "email" in user :
                USERS_DIC[user['email']]=user['userStatus']
    return ()

##################################
## USERS details
##################################
def detail_user(CLIENT_ID,TOKEN,EMAIL):

    uri=API_ACCOUNT+CLIENT_ID+'/users/'+EMAIL

    datastore = queryDynatraceAPI(uri,TOKEN)
    print(datastore['email'])
    print(datastore['groups'])

    return ()

##################################
## Create USER
##################################
def create_user(CLIENT_ID,TOKEN,email):

    payload={
            "email": email
            }
    
    uri=API_ACCOUNT+CLIENT_ID+'/users'
    print(' '+email)
    result = postDynatraceAPI(uri,payload,TOKEN)
    #print(result)
    print(' => create user: '+email)
        
    return ()

##################################
## add USER to user group
##################################
def add_user_to_ug(CLIENT_ID,TOKEN,ugid,email):

    payload=[
            ugid
            ]
    
    uri=API_ACCOUNT+CLIENT_ID+'/users/'+email
    postDynatraceAPI(uri,payload,TOKEN)
    print(' => add user: '+email+' to user group '+ugid)
        
    return ()

##################################
## Main program
##################################
IAM_Token=iam_token()
list_env(AccountUiid,IAM_Token)
list_groups(AccountUiid,IAM_Token)
list_users(AccountUiid,IAM_Token)

#print('IAM')
#print(' AccountUiid',AccountUiid)
#print(' IAM_Token',IAM_Token[0:10]+'...')

print('Target')
print(' Emails',Email)
print(' based one project: ',Management_Zone)

#step 1 - Prerequisite :  management zone must exist in the tenant. If not exit with error 
print('step 1 - perequisite management zone exist')
#if Management_Zone not in MZ_DIC.values() :
#    sys.exit('error '+Management_Zone+ ' doesn t exist - create management zone first')
i=0
while Management_Zone not in MZ_DIC.values() :
    print('waiting for management zone: \"'+Management_Zone+'\" to be created first')
    time.sleep(wait)
    list_env(AccountUiid,IAM_Token)
    i+=1

    if i >= 30 :
        sys.exit('timeout after '+str(30*wait)+' seconds')


#step 2 - Is management zone exists as User Group ? if not create it.
print('step 2 - create new user groups')
if Management_Zone not in GROUPS_DIC:
    #print('to create')
    Result=create_group(AccountUiid,IAM_Token,Management_Zone)
    groupUuid=Result[0]['uuid']
else :
    groupUuid=GROUPS_DIC[Management_Zone]

#print(groupUuid)

#step 3 - map user group to management zone for ech tenant
print('step 3 - apply new permissions')
permissions=[]
for mzid in MZ_DIC:
    if MZ_DIC[mzid] == Management_Zone :
        print(' ',mzid)
        for permissionName in PERMISSION_LIST:
            permission= {
                "permissionName": permissionName,
                "scope": mzid,
                "scopeType": "management-zone"
                }
            permissions.append(permission)


if permissions != []:
    #print(permissions)
    map_mz_ug(AccountUiid,IAM_Token,groupUuid,permissions)
    
#step 4 - test if user is created
print('step 4 - create new users')
for email in Email :
    if email not in USERS_DIC :
        create_user(AccountUiid,IAM_Token,email)
        
i=0
list_users(AccountUiid,IAM_Token)
while email in Email and not list_users :
    time.sleep(wait)
    list_users(AccountUiid,IAM_Token)
    i+=1

    if i >= 30 :
        sys.exit('timeout create user '+email+ ' after '+str(30*wait)+' seconds')

#step 5 - add users to user group
print('step 5 - add users to user group')
for email in Email :
    add_user_to_ug(AccountUiid,IAM_Token,groupUuid,email)
    

print("###")

