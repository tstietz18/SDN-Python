# ---------------------------------------------------------
#Name: Unit 3 Lab
#      
#Author:Tory Stietz    
# 
#Date created: 2/13/2021
# 
#Script Function1: Asks a user for their first and last name, saves first and last name as a variable.
#Script Function2: Have the script welcome them by replying "Welcome to Python, firstname. Lastname is a really interesting surname! Are you related to the famous Victoria lastname?”
# 
#Script References: W3schools.com/python
# 
#Special Instructions: Enter desired username when prompted to do so.
#
#****************************

ntpServer = {
   
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6"

    }

print(ntpServer)

def PingPrep(ipList):
    
    print("ping " + ntpServer[ipList]["ServerIP"])

keystring = ""

for key in ntpServer.keys():
    print("key = " + key + " \t value = " + ntpServer[key])
    keystring = keystring + "\t" + key

'''
'''
for ipList in ntpServer.keys():
    print("ping " + ntpServer[ipList])


devices = {
    "R1": {
        "type": "router",
        "hostname": "R1",
        "mgmtIP": "10.0.0.1"

        },
    "R2": {
        "type": "router",
        "hostname": "R2",
        "mgmtIP": "10.0.0.2"

        },
    "S1": {
        "type": "switch",
        "hostname": "S1",
        "mgmtIP": "10.0.0.3",

        },
    "S2": {
        "type": "switch",
        "hostname": "S2",
        "mgmtIP": "10.0.0.4"

        }
    }
          
        # create a list of strings and add ping
deviceList = []
for key in devices.keys():
    deviceList.append('ping ' + devices[key]['mgmtIP'])
          

          #print the list
for dev in deviceList:
    print(dev)

#def pingPrepDev(devices):

#ask user if they want to add device

HostName = input("Add a New Device Hostname")
devType= input("Add a New Device Type")
IpAddress = input("Add a New Address")

#if yes enter type, hostname, mgmtIP --> Verify valid IP


def validIP(IPaddr) :

    if number.isnumeric() == True :
        if int(IPaddr) >= 1 and int(IPaddr) <= 4:
            return True
        else : False

#Add new device to devices dictionary
devices[HostName] = {
    " type ": devType,
    " hostname ": HostName,
    " mgmtIP ": IpAddress

    }

print(devices)
