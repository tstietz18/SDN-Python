'''
name: final-ios.py
author: scout mitchell
date created: 4/29/21
script function: filters through iosxe devices in cml. adds 15 to 2nd octect
                 then modifies current config with new ip's. adds new ospf
                 instance with added 15 then deletes original ospf instance.
                 re-outputs tables with updated info
'''

#modules! modules! modules!
import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict
import requests
import json

def shIP(switch): #sh ip int br
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

#interface list output with int name, ip address, subnet
def ipList(ints):
    print(i+' Interfaces:\n')
    print('Interface\t\tIP add\t\tSubnet')
    print('-'*55)

    for interface in ints.keys():
        print(interface+'\t'+ints[interface]['add']+'\t'+ints[interface]['sub'])

def add15(ints): #adds 15 to 2nd octet
    for key in ints.keys():
        ipSplit=ints[key]['add'].split('.')
        octet=int(ipSplit[1])+15
        ipSplit[1]=octet
        newIP=ipSplit[0]+'.'+str(octet)+'.'+ipSplit[2]+'.'+ipSplit[3] #put the split back together
        ints[key]['add']=newIP #replaces 'ints' dict keys with new addresses
    return ints

def changeInt(switch,ints): #changes interface to match add15
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
        
def changeOSPF(switch): #add15 but ospf (hard coded cuz im lazy)
    router = {"host": switch, "port" : "830",
          "username":"cisco","password":"cisco"}
    
    xmlInt = """
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <router>
                    <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                      <id>1</id>
                        <network>
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

    #Parse returned XML to Dictionary
    #netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]

def showOSPF(switch): #show ospf info
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

def deleteOSPF(switch): #delete original ospf network...hard-coded again
    router = {"host": switch, "port" : "830",
          "username":"cisco","password":"cisco"}
    
    xmlInt = """
    <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <router>
                    <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                      <id>1</id>
                        <network operation='delete'>
                            <ip>172.16.252.0</ip>
                            <mask>0.0.3.255</mask>
                            <area>0</area>
                        </network>  
                    </ospf>
                </router>
            </native>
    </config>"""

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.edit_config(target = 'running', config = xmlInt)

'''
main
'''

#iiterate thru dict in .json file
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
