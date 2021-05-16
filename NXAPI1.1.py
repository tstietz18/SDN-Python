# ---------------------------------------------------------
#Name: Nexos Sandbox 2
#      
#Author:Tory Stietz    
# 
#Date created: 5/5/2021
# 
#Script Function: Ask for a hostname
# 
#Script References:
# 
#Special Instructions:
#
#****************************

import requests
import json

def ChangeHostName(NewHostName):
   
    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='http://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "configure terminal",
        "version": 1
        },
        "id": 1
    },
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "hostname" + NewHostName,
        "version": 1
        },
        "id": 2
    }
    ]

    '''

    verify=False below is to accept untrusted certificate

    '''

    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

    #return response
    
#Main Code

NewHostName = input("Enter a new hostname:")


#function to Validate a Hostname
def isvalidhostname(HostName):
    if HostName[0].isalpha() != True:
        return False
    if HostName[0].isdigit() == True:
        return False
    if len(HostName) <=0 or len(HostName) >= 64:
        return False
    for character in HostName:
        if character.isalnum() != True and character != '-':
            return False
     
    return True

#Hard coded hostname stored in validhost variable.
HostName = 'R-1'
validhost = isvalidhostname(HostName)
print(validhost)

#if the hostname is valid it is passed here and printed.
validHost = False
while validHost == False:
    HostName = input("What do you want to name this device?:")
    print("Host Name is:" + HostName)

    validHost = isvalidhostname(HostName)
    if validHost == False:
        print("Enter a Valid Hostname")
getisvalidhostname(HostName)


