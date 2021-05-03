import requests
import json

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
    

