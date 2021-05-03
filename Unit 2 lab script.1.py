# ---------------------------------------------------------
#Name: Unit 2 Lab.1
#      
#Author:Tory Stietz    
# 
#Date created: 1/27/2021
# 
#Script Function: 
# 
#Script References:
# 
#Special Instructions:
#
#****************************


#Creating dictionary entries
router1 = {
    "brand": "Cisco",
    "model": "1941",
    "hostname": "R1",
    "mgmtIP": "10.0.0.1 255.255.255.0",
    "G0/0": "10.0.1.1 255.255.255.0",
    "G0/1": "10.0.2.1 255.255.255.0",
    "G0/2": "10.0.3.1 255.255.255.0",
    
    }
#find out how to incorporate subnets (keep in mind length of line might be an issue."

print(router1)
print(router1.keys())
print(router1.values())
print(router1.items())

#ip = router1["mgmtIPAddress"]
#ip = router1["G0/0IPAddress"]
#ip = router1["G0/1IPAddress"]
#ip = router1["G0/2IPAddress"]
#review keys, not sure of context.


# end of script

