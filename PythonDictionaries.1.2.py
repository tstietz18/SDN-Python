# ---------------------------------------------------------
#Name: Python Dictionaries.1
#      
#Author:Tory Stietz    
# 
#Date created: 1/27/2021
# 
#Script Function: Create a dictionary with an embedded dictionary in it.
# 
#Script References:
# 
#Special Instructions:
#
#****************************

router1 = {
    "hostname": "R1",
    "brand": "Cisco",
    "mgmtIP": "10.0.0.1",
    "interfaces": {
                    "G0/0": "10.1.1.1",
                    "G0/1": "10.1.2.1"
                  }

            }
#the following two command segements will print what the items in parentheses are (ex: dictionary, string, integer)
type(router1)

type(router1["interfaces"])

# the following two command segments will pringt the contents of the dictionaries.
print(router1)

print(router1["interfaces"])

# these three command segments will print the keys, values, and items of the router1 dictionary.
print(router1.keys())

print(router1.values())

print(router1.items())

# the next three command segments will print only the keys, values, and items of the embedded dictionary.
print(router1["interfaces"].keys())

print(router1["interfaces"].values())

print(router1["interfaces"].items())

# these two command segments will print the value of the key labeled with the interface names.
print(router1["interfaces"]["G0/0"])

print(router1["interfaces"]["G0/1"])

# the following for loop will iterate through all the keys and values in the embedded dictionary "interfaces".
for interface in router1["interfaces"]:
    print(interface + " " * 5 + router1["interfaces"][interface])

#dictionary inception

devices = {
    "R1" : {
    "type" : "Router",
    "hostname" : "R1",
    "mgmtIP" : "10.0.0.1"
    },
    "R2" : {
        "type" : "Router",
        "hostname" : "R2",
        "mgmtIP" : "10.0.0.1"
    },
    "S1" : {
        "type" : "Switch",
        "hostname" : "S1",
        "mgmtIP" : "10.0.0.3"
    },
    "S2" : {
        "type" : "Switch",
        "hostname" : "S2",
        "mgmtIP" : "10.0.0.4"
        }
}

for device in devices.keys:
    print(device 


    



