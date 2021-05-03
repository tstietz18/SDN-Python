

import requests
import json

"""
Modify these please
"""
switchuser='cisco'
switchpassword='cisco'

url='https://10.10.20.177/ins'
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
response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()

# prints the full dictionary
print(response)

host = 'host_name'
print('Hostname = ' + response['result']['body'][host])

mem = 'memory'
print('Memory = ' + str(response['result']['body'][mem]))

mtype = 'mem_type'
print('Memory-Type = ' + response['result']['body'][mtype])
