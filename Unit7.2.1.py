import requests
import json

def GetIpInterfaceBrief():
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
          "cmd": "show ip interface brief",
          "version": 1
        },
        "id": 1
      }
    ]

    '''

    verify=False below is to accept untrusted certificate

    '''

    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

    print(response)#prints the full dictionary.
    
    interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]

    for interface in interfaces:
        print(interface['intf-name']) #individually prints each nested dictionary within the main dictionary.

    #prints the headings inside the parthenses spaced out with the \t tabs
    print("Name\t\tProtocol\tLink\t\tAddress")
    #prints 60 dashes to act as a divider between the headings and the actual device information.
    print("-" * 60)

    #references the section of command that says interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]
    for info in interfaces :
    #Prints the info stored in interfaces for each specified key from the nested dictionary.
       print(info['intf-name'] + '\t\t' + info['proto-state'] + '\t\t' + info['link-state'] + '\t\t' + info['prefix'])

    return response

#Changes the IP Address and Subnet Mask.
def ChangeIpAddressAndSubnet(InterfaceName, NewIpAddress, SubnetMask):
    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
            "cmd": "config terminal",
            "version": 1
            },
            "id": 1
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
            "cmd": "interface " + InterfaceName,
            "version": 1
            },
            "id": 2
        },
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
            "cmd": "ip address " + NewIpAddress + SubnetMask,
            "version": 1
            },
            "id": 3
        }
        ]

    '''

    verify=False below is to accept untrusted certificate

    '''

    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

def ValidateIP(newIP):
    
    if len(ipList) == 4:
        validEntry = True
    else:
        return False
    if validEntry == True:
        for Octet in ipList:
            if Octet.isdigit() == False:
                return False
    if validEntry == True:
        for Octet in ipList:
            if int(Octet) < 0 or int(Octet) > 255:
                return False
    return True


def checkInt(InterfaceName, response):
    interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]

    for interface in interfaces:
        if InterfaceName == interface['intf-name']: #individually prints each nested dictionary within the main dictionary.
            return True
    
    return False

def ValidateSubnetMask(newSubnet):
    if len(ipList) == 4:
        validEntry = True
    else:
        return False
    if validEntry == True:
        for Octet in ipList:
            if Octet.isdigit() == False:
                return False
    if validEntry == True:
        for Octet in ipList:
            if int(Octet) < 0 or int(Octet) > 255:
                return False
    return True

        ### MAIN CODE ###
response = GetIpInterfaceBrief()

#Validates that the interface exists.
validInt = False
while validInt == False:
    InterfaceName = input("Enter a Interface Name")
    validInt = checkInt(InterfaceName, response)
    if validInt == False:
        print("Enter a valid interface name")
while True:
    ipAddr = input("Enter a new IP Address")
    if ValidateIP(ipAddr) == True:
        break
    else:
        print("That is a Bad address!")        
while True:
    SubnetMask = input("Enter a valid subnet mask:")
    if ValidateSubnetMask(Subnet) == True:
        break
    else:
        print("Enter a Valid Subnet Mask!")
                      
                      
#Ask the user to change the IP Address.
    NewIpAddress= input("Enter another valid Ip Address:")
    print(NewIpAddress)





#print(ChangeIpAddressAndSubnet)

