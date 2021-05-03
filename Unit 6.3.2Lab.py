import requests
import json

def getDeviceInfo(ipAddr):

    """
    Be sure to run feature nxapi first on Nexus Switch

    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + ipAddr + '/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show version",
          "version": 1
        },
        "id": 1
      }
    ]

    '''

    verify=False below is to accept untrusted certificate

    '''

    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

    print(response)
    return response


#main code


    
print('Host\t\tMemory\t\tMemory Type\tChassis\t\t\tBoot File Name')

print('-' * 100)

###dictionary to store information that will be a part of a for loop at a later step.
##device_info = {
##    "response" : getDeviceInfo('10.10.20.177'),
##    "devices" : response['result']['body'],
##    "memory" : str(devices['memory'])
##    }

##for devinf in device_info:
##    print(d

response = getDeviceInfo('10.10.20.178')

devices = response['result']['body']

memory = str(devices['memory'])       

#for switch in devices:
print(devices['host_name'] + '\t' + memory + '\t\t' + devices['mem_type'] + '\t' + devices['chassis_id'] + '\t\t' + devices['kick_file_name'])



