# ---------------------------------------------------------
#Name: Nexos Sandbox 2
#      
#Author:Tory Stietz    
# 
#Date created: 5/5/2021
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
      "cmd": "hostname dist-sw01-9k",
      "version": 1
    },
    "id": 2
  }
]
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()



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
getNewHostName(HostName)

#Asks the user to enter an Ip address and splits it into four integers.
IpAddress= input('Enter a new IP Address:')
print IpAddress

ipList =  IpAddress.split(".")

#Adds two to the new Ip Address and prints the Address.
def AddToIP(ipList):

    octet3 = int(myList[2])
    octet3 = octet3 + 2
    myList[2] = str(octet3)

    newIP = myList [0] + "." + myList[1] + "." + myList[2] + "." + myList[3]

    print("newIP")

#Validates the new Ip Address.
def ValidateIp(newIP):
    
    if len(ipList) == 4:
        validEntry = True
    else:
        validEntry = False
    if validEntry == True:
        for Octet in ipList:
            if Octet.isdigit() == False:
                validEntry = False
    if validEntry == True:
        for Octet in ipList:
            if int(Octet) < 0 or int(Octet) > 255:
                validEntry = False
    if validEntry == True :
        print("That is a Valid IP")
    else:
         print("Enter a Valid Ip")

def GetNewIpAddress(IpAddress + SubnetMask)

    """
    Be sure to run feature nxapi first on Nexus Switch

    """
    #sets the username and password to the values in the single quotations.
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc{
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
              "cmd": "ip address " + IpAddress + SubnetMask,
              "version": 1
             },
            "id": 2
          }
        ]
      
    '''

    verify=False below is to accept untrusted certificate

    '''



##"10.1.1.254"
##
##['10','1','1','254']
##
##
##octet3 = int(myList[2])
##octet3 = octet3 + 2
##myList[2] = str(octet3)
##
##newIP = myList [0] + "." + myList[1] + "."  etc..

# end of script
