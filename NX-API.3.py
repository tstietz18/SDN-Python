# ---------------------------------------------------------
#Name: Nexos Sandbox 2
#      
#Author:Tory Stietz    
# 
#Date created: 4/21/2021
# 
#Script Function: 
# 
#Script References:
# 
#Special Instructions:
#
#****************************

import requests
import json

NewHostName = input("Enter a new hostname:")

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

HostName = 'R-1'
validhost = isvalidhostname(HostName)
print(validhost)
   
def getNewHostName(HostName): 

    """
    Be sure to run feature nxapi first on Nexus Switch

    """
    #sets the username and password to the values in the single quotations.
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
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
    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

    '''

    verify=False below is to accept untrusted certificate

    '''
validHost = False
while validHost == False:
    HostName = input("What do you want to name this device?:")
    print("Host Name is:" + HostName)

    validHost = isvalidhostname(HostName)
    if validHost == False:
        print("Enter a Valid Hostname")
        



# end of script
