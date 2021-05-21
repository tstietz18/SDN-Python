# ---------------------------------------------------------
#Name: Unit 7 Lab 1
#      
#Author:Tory Stietz    
# 
#Date created:5/18/2021
# 
#Script Function: Change an IP Address
# 
#Script References: Unit 7
# 
#Special Instructions:
#
#****************************

import requests
import json

NexosSwitches = {
    "dist-sw01" : {
        "hostname" : "dist-sw01",
        "devicetype" : "switch",
        "mgmtIP" : "10.10.20.177"
        },
    "dist-sw02" : {
        "hostname" : "dist-sw02",
        "devicetype" : "switch",
        "mgmtIP" : "10.10.20.178"
        }
}

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


def changeIpAddress(deviceIP, intName, ipAddr):

    """
    Be sure to run feature nxapi first on Nexus Switch

    """
    #sets the username and password to the values in the single quotations.
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + deviceIP + '/ins'
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
        "cmd": "interface " + intName,
        "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "ipaddress " + ipAddr + " 255.255.255.0",
        "version": 1
        },
        "id": 3
      }
    ]

    '''

    verify=False below is to accept untrusted certificate

    '''

    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

    return response

response = getipInterfaceBrief

print("Name\t\tProtocol\tLink\t\tAddress")

ipInterfaceBrief = response["result"]["body"]["TABLE_intf"]["ROW_intf"]

print("-" * 60)

for interface in interfaces:
    print(interface['intf-name']) #individually prints each nested dictionary within the main dictionary.

#references the section of command that says interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]
for info in interfaces :
#Prints the info stored in interfaces for each specified key from the nested dictionary.
   print(info['intf-name'] + '\t\t' + info['proto-state'] + '\t\t' + info['link-state'] + '\t\t' + info['prefix'])


#MAIN CODE
#print(response)#prints the full dictionary.



#Refernces the dictionanry NexosSwitches to get the management ip.
for key in NexosSwitches.keys():
    IPInterfaceBrief = getIPInterfaceBrief(NexosSwitches[key]['mgmtIP'])
    print(IPInterfaceBrief)
    
#Asks the user which interface ip the want to change.
interfacename = input("Which interface address would you like to change:")
print("Interface is:" + interfacename)


""" #Validates the interface name and allows us to change the ip address???
validHost = False
while validHost == False:
    HostName = input("What do you want to name this device?:")
    print("Host Name is:" + HostName)

    validHost = isvalidhostname(HostName)
    if validHost == False:
        print("Enter a Valid Hostname")
getNewHostName(HostName)
 """

#Asks the user to enter a new ip address and splits it into a string so it can be verified.
IpAddress= input('Enter a new IP Address:')
print(IpAddress)

ipList =  IpAddress.split(".")

#Adds two to the new Ip Address and prints the Address.
def AddToIP(ipList):

    octet3 = int(myList[2])
    octet3 = octet3 + 2
    myList[2] = str(octet3)

    newIP = myList[0] + "." + myList[1] + "." + myList[2] + "." + myList[3]

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
         print("Enter a Valid IP")

# end of script
