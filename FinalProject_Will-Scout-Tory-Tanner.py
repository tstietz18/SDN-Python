'''***********************
Name: FinalProject_step-2.py
Author: Will Johnson, Scout Mitchell
Class Period: SDN Wednesday Night
Date Created: 05/05/2021
Script Function:  All tasks are completed using various automation models: NXAPI-DME, NXAPI-CLI and NETCONF
    NXOS: Filters through NXOS devices from a JSON file. The script then increases the second octet from 16 to 31. 
          All OSPF, HSRP and SVI instances are updated with the new addressing scheme.
          Lastly a user is asked to provide information for the addition of a given Vlan.

    IOS:  filters through iosxe devices in cml. adds 15 to 2nd octect
          then modifies current config with new ip's. adds new ospf
          instance with added 15 then deletes original ospf instance.
          re-outputs tables with updated info
***********************'''
# Import required modules
import requests
import re
import json
import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict
import requests
import json

# Static variables
username = "cisco"
password = "cisco"

#--- NXOS Functions ---#
# Define function to import device list
def getFile():
    with open('\\School\\SDN\\Assessment\\FinalProject\\devDict.json') as devDict:
        data = json.load(devDict)
        return data
# Define function to get the authentication cookie
def getCookie(addr,uname,pwd) :
    #NX REST API Authen See REST API Reference for format of payload below
    url = "https://"+ addr +"/api/aaaLogin.json"
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : uname,
                    "pwd" : pwd}
               }
          }
    response = requests.post(url, json=payload, verify=False)
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
# Define function to get interface HSRP configuration
def getHSRP (addr,uname,pwd):
    url="https://"+addr+"/ins"
    headers={'content-type':'application/json-rpc'}
    payload=[
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
            "cmd": "show hsrp",
            "version": 1
            },
            "id": 1
        }
    ]
    response = requests.post(url,data=json.dumps(payload),verify=False,headers=headers,auth=(uname,pwd)).json()

    for hsrpInfo in response["result"]["body"]["TABLE_grp_detail"]["ROW_grp_detail"]:
        vipSplit = hsrpInfo["sh_vip"].split(".")
        vipSplit[1] = 31
        vipCombined = ""
        for octet in vipSplit:
            vipCombined = vipCombined + str(octet) +"."
        vipCombined = vipCombined.rstrip(".")
        hsrpInfo["sh_vip"] = vipCombined

    return(response["result"]["body"]["TABLE_grp_detail"]["ROW_grp_detail"])
# Define function to get interface IP configuration
def getIntf(addr,uname,pwd):
    url="https://"+addr+"/ins"
    headers={'content-type':'application/json-rpc'}
    payload=[
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
            "cmd": "show ip int bri",
            "version": 1
            },
            "id": 1
        }
    ]

    response = requests.post(url,data=json.dumps(payload),verify=False,headers=headers,auth=(uname,pwd)).json()
    
    for intf in response["result"]["body"]["TABLE_intf"]["ROW_intf"]:
        ipsplit = intf["prefix"].split(".")
        ipsplit[1] = 31
        ipCombined = ""
        for octet in ipsplit:
            ipCombined = ipCombined + str(octet) +"."
        ipCombined = ipCombined.rstrip(".")
        intf["prefix"] = ipCombined

    return(response["result"]["body"]["TABLE_intf"]["ROW_intf"])
# Define function to create the desired vlan and name it
def postVlan(addr,token,vlId,vlName):
    url = "https://"+addr+"/api/mo/sys.json"
    payload = {
        "topSystem": {
            "children": [{
                "bdEntity": {
                "children": [{
                    "l2BD": {
                        "attributes": {
                        "fabEncap": vlId,
                        "name": vlName
                        }
                      }
                    }
                  ]
                }
              }
            ]
          }
      }
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'APIC-cookie='+token
        }
    return bool(requests.post(url, headers=headers, json=payload, verify=False))
# Define function to assign an IP to the SVI and enable the interface
def postSVI(addr,token,sviId,sviAddr,subnet):
    url = "https://"+addr+"/api/node/mo/sys.json"
    payload = {
      "topSystem": {
        "children": [
        {
            "ipv4Entity": {
              "children": [
                {
                "ipv4Inst": {
                    "children": [
                    {
                        "ipv4Dom": {
                          "attributes": {
                            "name": "default"
                        },
                        "children": [
                            {
                            "ipv4If": {
                                "attributes": {
                                  "id": sviId
                                },
                                "children": [
                                {
                                    "ipv4Addr": {
                                      "attributes": {
                                        "addr": sviAddr+subnet
                                      }
                                    }
                                  }
                                ]
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          },
        {
            "interfaceEntity": {
            "children": [
                {
                "sviIf": {
                    "attributes": {
                    "adminSt": "up",
                    "id": sviId
                    }
                  }
                }
              ]
            }
          }
        ]
      }
     }
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'APIC-cookie='+token
        }
    return bool(requests.post(url, headers=headers, json=payload, verify=False))
# Define function to add/modify HSRP on an interface
def postHSRP(addr,token,hsrpIP,hsrpId,vlId):
    url = "https://"+addr+"/api/node/mo/sys.json"
    payload = {
      "topSystem": {
        "children": [{
            "interfaceEntity": {
              "children": [{
                "sviIf": {
                    "attributes": {
                      "id": vlId
                    }
                  }
                }
              ]
            }
          },
        {
            "hsrpEntity": {
              "children": [{
                "hsrpInst": {
                    "children": [{
                        "hsrpIf": {
                          "attributes": {
                            "id": vlId
                        },
                        "children": [{
                            "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "id": hsrpId,
                                  "ip": hsrpIP
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
     }
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'APIC-cookie='+token
        }
    return bool(requests.post(url, headers=headers, json=payload, verify=False))
# Define function to assign an interface to area 0 of OSPF instance 1
def postOSPF(addr,token,pid,area,sviId):
    url = "https://"+addr+"/api/node/mo/sys.json"
    payload = {
      "topSystem": {
          "children": [{
            "ospfEntity": {
              "children": [{
                "ospfInst": {
                    "attributes": {
                      "name": pid
                    },
                    "children": [{
                        "ospfDom": {
                          "attributes": {
                            "name": "default"
                        },
                        "children": [{
                            "ospfIf": {
                                "attributes": {
                                  "advertiseSecondaries": "yes",
                                  "area": area,
                                  "id": sviId
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          },
        {
            "interfaceEntity": {
            "children": [
                {
                "sviIf": {
                    "attributes": {
                    "id": sviId
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'APIC-cookie='+token
        }
    return bool(requests.post(url, headers=headers, json=payload, verify=False))

#--- IOS-XE Functions ---#
# Define function to show ip interface brief
def shIP(switch):
    router = {"host": switch, "port" : "830",
          "username":"cisco","password":"cisco"}
    
    netconf_filter = """
    <filter>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>          
            </interface>
        </interfaces>
    </filter>"""

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.get_config(source = 'running', filter = netconf_filter)

    #Parse returned XML to Dictionary
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    #Create List of Interfaces
    interfaces = netconf_data["interfaces"]["interface"]

    intDict={} #interface dictionary for final output
    
    for interface in interfaces: #add to ints dict
        if 'GigabitEthernet1' not in interface['name']: #exclude mgmtip
            if 'address' in interface['ipv4']: #only adds to dictionary if interface has an address
                intDict[interface['name']] = {'add': interface['ipv4']['address']['ip'], 'sub': interface['ipv4']['address']['netmask']}
    return intDict
# Define function to list interface output with int name, ip address, subnet
def ipList(ints):
    print(i+' Interfaces:\n')
    print('Interface\t\tIP add\t\tSubnet')
    print('-'*55)

    for interface in ints.keys():
        print(interface+'\t'+ints[interface]['add']+'\t'+ints[interface]['sub'])
# Define function to add 15 to 2nd octet
def add15(ints):
    for key in ints.keys():
        ipSplit=ints[key]['add'].split('.')
        octet=int(ipSplit[1])+15
        ipSplit[1]=octet
        newIP=ipSplit[0]+'.'+str(octet)+'.'+ipSplit[2]+'.'+ipSplit[3] #put the split back together
        ints[key]['add']=newIP #replaces 'ints' dict keys with new addresses
    return ints
# Define function to change interfaces to match add15
def changeInt(switch,ints):
    router = {"host": switch, "port" : "830",
              "username":"cisco","password":"cisco"}

    for key in ints:
        xmlInt = """<config>
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                <interface>
                                    <%intName%>
                                        <name>%intNum%</name>				
                                        <ip>                                    
                                            <address>
                                                <primary>
                                                    <address>%addr%</address>
                                                    <mask>%mask%</mask>
                                                 </primary>
                                            </address>                                   
                                        </ip>				
                                    </GigabitEthernet>
                                </interface>		    
                        </native>
                </config>"""     

        xmlInt = xmlInt.replace("%addr%", ints[key]['add'])
        xmlInt = xmlInt.replace("%intName%", key[0:-1]) #interface sans number
        xmlInt = xmlInt.replace("%intNum%", key[-1]) #interface number
        xmlInt = xmlInt.replace("%mask%", ints[key]['sub'])
    
        with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
            netconf_reply = m.edit_config(target = 'running', config = xmlInt)
# Define function to add15 but ospf (hard coded cuz im lazy)
def changeOSPF(switch):
    router = {"host": switch, "port" : "830",
          "username":"cisco","password":"cisco"}
    
    xmlInt = """
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <router>
                    <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                      <id>1</id>
                        <network>
                            <ip>172.46.252.0</ip>
                            <mask>0.0.3.255</mask>
                            <area>0</area>
                        </network>  
                    </ospf>
                </router>
            </native>
        </config>"""

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.edit_config(target = 'running', config = xmlInt)

    #Parse returned XML to Dictionary
    #netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]
# Define function to show ospf info
def showOSPF(switch):
    router = {"host": switch, "port" : "830",
          "username":"cisco","password":"cisco"}
    
    netconf_filter = """
    <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <router>
                    <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf"> 
                    </ospf>
                </router>
            </native>
    </filter>"""

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.get_config(source = 'running', filter = netconf_filter)  
      
    #Parse returned XML to Dictionary
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]['data']['native']['router']['ospf']
    network=netconf_data['network']

    #a nice table
    print(i+' OSPF Process '+netconf_data['id'])
    print('-'*66)
    print('Network: '+network['ip']+'\t\t'+'Mask: '+network['mask']+'\t\t'+'Area: '+network['area']+'\n')
# Define function to delete original ospf network...hard-coded again
def deleteOSPF(switch):
    router = {"host": switch, "port" : "830",
          "username":"cisco","password":"cisco"}
    
    xmlInt = """
    <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <router>
                    <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                      <id>1</id>
                        <network operation='delete'>
                            <ip>172.31.252.0</ip>
                            <mask>0.0.3.255</mask>
                            <area>0</area>
                        </network>  
                    </ospf>
                </router>
            </native>
    </config>"""

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.edit_config(target = 'running', config = xmlInt)

#--- Global functions ---#
# Define function to validate user IP address input
def isValidIp(ip):
    testIP = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(testIP) and all(map(lambda n: 0 <= int(n) <= 255, testIP.groups()))
# Define funtion to valiate user subnet mask input
def isValidMask(mask):
    testMask = re.match(r"^/(\d{1,2})$", mask)
    return bool(testMask)

"""
Main Script
"""
# Import the device list file
devDict = getFile()

# Loop through each device in a file and make changes to the devices.
for device in devDict.keys():
    if devDict[device]["devicetype"] == "NXOS":
        print("Device type is NXOS.\n")
        ipAddress = devDict[device]["mgmtIP"]
        token = getCookie(ipAddress, username, password)
        intfList = getIntf(ipAddress, username, password)
        hsrpList = getHSRP(ipAddress, username, password)
        print("All interfaces on "+device+" will be changed from 172.16.0.0 addressing to 172.31.0.0 addressing.")
        print("All HSRP instances will have their VIPs updated to the new addressing scheme.")
        for interface in intfList:
            intfName = (interface["intf-name"]).lower()
            sviAddress = interface["prefix"]
            subnet = "/24"
            print("Attempting to modify interface "+intfName)
            if postSVI(ipAddress, token, intfName, sviAddress, subnet) is True:
                print("Request completed successfully!\n")
            else:
                print("Request failed!\n")
        for interface in hsrpList:
            vlId = (interface["sh_if_index"]).lower()
            hsrpIP = interface["sh_vip"]
            hsrpId = interface["sh_group_num"]
            print("Attempting to modify HSRP info on interface "+vlId)
            if postHSRP(ipAddress, token, hsrpIP, hsrpId, vlId) is True:
                print("Request completed successfully!\n")
            else:
                print("Request failed!\n")
        # The following section deals with the addition of Vlan120 and asking the user for various input to configure the new Vlan
        while True:
            print("This sections is to add VLAN120 to NXOS device: "+device+". Please be ready to input a valid IP and Subnet mask, as well as, an HSRP Address.")
            userIntfName = input("Please enter a name for the interface: ")
            userIP = input("Please enter a valid IP address (x.x.x.x): ")
            while isValidIp(userIP) is True:
                userMask = input("Please enter a valid subnet mask (/24): ")
                while isValidMask(userMask) is True:
                    userHSRPip = input("Please enter a valid HSRP VIP (y.y.y.y): ")
                    userHSRPid = input("Please enter a HSRP group id to be used: ")
                    while isValidIp(userHSRPip) is True:
                        intfName = "vlan120"
                        postVlan(ipAddress, token, "vlan-120", userIntfName)
                        postSVI(ipAddress, token, intfName, userIP, userMask)
                        postHSRP(ipAddress, token, userHSRPip, userHSRPid, intfName)
                        postOSPF(ipAddress, token, "1", "0.0.0.0", intfName)
                        break
                    break
                break
            break

print("Device type is IOS-XE.\n")
with open('devdict.json') as json_file:
    data=json.load(json_file)

    for i in data.keys():
        if data[i]['devicetype']=='IOSXE':
            ipList(shIP(data[i]['mgmtIP']))
            print('\n\n')
            showOSPF(data[i]['mgmtIP'])
            print('\nUpdating system...\n')
            add15(shIP(data[i]['mgmtIP']))
            changeInt(data[i]['mgmtIP'],add15(shIP(data[i]['mgmtIP'])))
            changeOSPF(data[i]['mgmtIP'])
            deleteOSPF(data[i]['mgmtIP'])
            print('\nUpdate complete!\n')
            print()
            ipList(shIP(data[i]['mgmtIP']))
            print('\n\n')
            showOSPF(data[i]['mgmtIP'])
            print('='*69+'\n')

            