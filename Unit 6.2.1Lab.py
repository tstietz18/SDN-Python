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

print("Host\t\tType\t\tMgmtIP")
#prints Host, type, and MgmtIP with spaces to act as a header.

print('-' * 50)
#prints dashes to separate the header from the keys/values.

for switch in NexosSwitches.keys():
    print(NexosSwitches[switch]['hostname'] + '\t' + NexosSwitches[switch]['devicetype'] +  '\t\t' + NexosSwitches[switch]['mgmtIP']) 
#iterates through the NexosSwitches dictionary and prints each the value of each key in a table format. 



# end of script
