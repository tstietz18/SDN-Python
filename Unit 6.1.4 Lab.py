# ---------------------------------------------------------
#Name: Unit 6 Lab
#      
#Author:Tory Stietz    
# 
#Date created: 3/18/2021
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

#stores everything that is indented below in the function getOspfNeighbor and refernces the variable ipAddr from the url portion of the command.
def getOspfNeighbor1(ipAddr):
    
    """
    Be sure to run feature nxapi first on Nexus Switch

    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + ipAddr +'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show ip ospf nei",
          "version": 1
        },
        "id": 1
      }
    ]

    '''

    verify=False below is to accept untrusted certificate

    '''

    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

    #print(response)
    return response
#iterates through the NexosSwitches dictionary for both NXOS switches and prints the keys for each hostname.
for key in NexosSwitches.keys():
    print('neighbors for ' + NexosSwitches[key]['hostname'])
    print("Router-ID\t\tNeighbor-IP\t\tInterface")

    print("-" * 60)
#stores the function getOspfNeighbors(NexosSwitches[key]['mgmtIP']) in the neighbors variable.
    neighbors = getOspfNeighbor1(NexosSwitches[key]['mgmtIP'])

    #print(neighbors)
# stores the levels of dictionaries that we need to access the ospf neighbors into the devices variable.
    devices = neighbors['result']['body']['TABLE_ctx']['ROW_ctx']['TABLE_nbr']['ROW_nbr']
#calls the devices variable we created to print the ospf neighbors information in a table format.
    for device in devices:
        print(device['rid'] + '\t' + device['addr'] + '\t' + device['intf'])
   #print()




# end of script
