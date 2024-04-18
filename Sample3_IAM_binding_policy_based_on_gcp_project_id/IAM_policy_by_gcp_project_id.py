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

LIST_GCP_PROJECT=['gcpproject1','gcpproject2','gcpproject3']
POLICY_ID='c4a4f6f9-cc78-42ff-924d-b29ab55b8176'

##################################
## Variables
##################################
UG={}   
API_ACCOUNT='https://api.dynatrace.com/iam/v1/accounts/'
API_BINDING='https://api.dynatrace.com/iam/v1/repo/account/'
#API_BINDING_ENV='https://api.dynatrace.com/iam/v1/repo/environment/'
wait=0.1

MZ_DIC={}
ENV_DIC={}
GROUPS_DIC={}
USERS_DIC={}
PREFIX=[]

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


#generic function delete to call API with a given uri
def delDynatraceAPI(uri,TOKEN):
    head = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }
    jsonContent = None
    response = requests.delete(uri,headers=head,verify=False)
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
    scope='account-idm-write account-idm-read account-env-read account-env-write iam-policies-management iam:policies:write iam:policies:read iam:bindings:write iam:bindings:read iam:effective-permissions:read'
    r = requests.post(SSO_Endpoint+'?grant_type=client_credentials&client_id='+Client_ID+'&client_secret='+Client_Secret+'&resource='+Account_Urn+'&scope='+scope,headers=headers)
    #print(r.json())
    return(r.json()['access_token'])

##################################
## IAM token
##################################
def list_groups(CLIENT_ID,TOKEN):

    uri=API_ACCOUNT+CLIENT_ID+'/groups'

    datastore = queryDynatraceAPI(uri,TOKEN)
    #print(datastore)
    if datastore != []:
        for group in datastore['items']:
            if group['name'] in LIST_GCP_PROJECT :
                UG[group['name']]=group['uuid']
        
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
    UG[ugname]=result[0]['uuid']

    print(' => create user group: '+ugname)
        
    return (result)

##################################
## Mapp Policy with User GROUP
##################################
def binding_ug(CLIENT_ID,TOKEN,ugid,name):

    #uri=API_BINDING_ENV+TENANT_ID+'/bindings/'+POLICY_ID+'/'+ugid
    uri=API_BINDING+AccountUiid+'/bindings/'+POLICY_ID+'/'+ugid
    payload={ 
              "parameters": { 
              "name": name 
              }
            }
    result = postDynatraceAPI(uri,payload,TOKEN)


    print(' => binding ug: '+ugid+' with key =  '+name)
        
    return (result)


##################################
## Main program
##################################
IAM_Token=iam_token()
list_groups(AccountUiid,IAM_Token)
for key in LIST_GCP_PROJECT:
 name=key.split('_')[0]
 if name not in PREFIX :
     PREFIX.append(name)
#print(UG)


#create UG if not exists
for name in LIST_GCP_PROJECT:
 if name not in UG: 
    create_group(AccountUiid,IAM_Token,name)
    time.sleep(wait)
    
IAM_Token=iam_token()    
#bind UG
for name in PREFIX:
    binding_ug(AccountUiid,IAM_Token,UG[name],name)
'''

#verif
for ug in UG:
    print(ug)
    uri=API_BINDING_ENV+TENANT_ID+'/bindings/'+POLICY_ID+'/'+UG[ug]
    result = queryDynatraceAPI(uri,IAM_Token)
    print(result['policyBindings'])

#delete UG
for ug in UG :
    print('delete', ug)
    uri=API_ACCOUNT+AccountUiid+'/groups/'+UG[ug]
    delDynatraceAPI(uri,IAM_Token)
'''

print("###")
