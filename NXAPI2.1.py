

#Adds two to the new Ip Address and prints the Address.
def AddToIP(myList):

    octet3 = int(myList[2])
    octet3 = octet3 + 2
    myList[2] = str(octet3)

    newIP = myList[0] + "." + myList[1] + "." + myList[2] + "." + myList[3]

    return newIP

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

def GetNewIpAddress(IpAddress):

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
        "cmd": "interface " + IpAddress,
        "version": 1
        },
        "id": 2
      },
        ]
      
    '''

    verify=False below is to accept untrusted certificate

    '''
#Asks the user to enter an Ip address and splits it into four integers.
IpAddress= input('Enter a new IP Address:')
print(IpAddress)

ipList =  IpAddress.split(".")

newIP = AddToIP(ipList)

print(newIP)

## + "255.255.255.0"
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
