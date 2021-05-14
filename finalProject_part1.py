'''
##################################################
Script Name: finalProject_part1.py

Author: Tanner Paulsen, Tory Stietz

Date Created: 4/28/2021

Script Function: This script retrieves the information from a json file and displays it to the user in a more readable format. 
The user is then able to add, modify, or remove devices from the json file.

Script References: 

Special Instructions: 

##################################################
'''

import json

#checkIp verifies that an IPv4 Address is valid
def checkIp(ipv4):

    #validIP set to True and is set to False if it meets the conditions
    validIP = True

    #ipAdd is split at the periods into a list
    splitIP = ipv4.split(".")

    #If there are not four octets in the split list, validIP is set to False
    if len(splitIP) != 4:
        validIP = False

    #For each octet in the list, if any of them are not a number validIP is set to False
    for octet in splitIP:
        if octet.isnumeric() == False:
            validIP = False

    #If none of the other conditions were met and validIP is still True, each octet in the list is checked to see if it is a number between 0 and 255. If not, validIP is set to False
    if validIP == True:
        for octet in splitIP:
            if int(octet) < 0 or int(octet) > 255:
                validIP = False

    #Value of validIP is returned to main code
    return validIP

#getFile retrieves json file from location specified by the user
def getFile(file):
    with open(file) as devDict:
        data = json.load(devDict)
        return data

#printDev takes user's json file to display devices to the user in a format that is easy to read
def printDev(json):
    print('Host' + '\t\t' + 'Type' + '\t' + 'IP')
    print('-' * 50)
    devList = ""
    devNum = 0

    #Device information is retrieved from the json and saved in devList which formats the data
    for device in json:
        if len(json[device]['hostname']) > 7:
            devList = devList + json[device]['hostname'] + '\t' + json[device]['devicetype'] + '\t' + json[device]['mgmtIP'] + '\n'
        else:
            devList = devList + json[device]['hostname'] + '\t\t' + json[device]['devicetype'] + '\t' + json[device]['mgmtIP'] + '\n'
    print(devList)

    #devList is returned to be used by other functions
    return devList

#getDev takes the user json as an argument to retrieve and format the device information, but does not display it like printDev does
def getDev(json):
    devList = ""
    devNum = 0

    #Device information is retrieved from the json and saved in devList which formats the data
    for device in json:
        devList = devList + json[device]['hostname'] + '\t' + json[device]['devicetype'] + '\t' + json[device]['mgmtIP'] + '\n'

    #devList is returned to be used by other functions
    return devList

#checkType checks that the Type entered by the user is either NXOS or IOSXE
def checkType(type):

    #If the user enters a '-' in the type name, it is removed
    replaceType = type.replace('-','')
    if replaceType.isalpha():

        #capsType converts type to all uppercase to match what is already in the json file
        capsType = replaceType.upper()
        if capsType == 'NXOS' or capsType == 'IOSXE':

            #Returns True if all parameters in function match
            return True
    
#validHost checks that a hostname entered by a user is valid and that it is NOT already in the json file
def validNewHost(host, file):

    validHostname = True
    
    #Each letter of the hostname entered by the user is split into a list
    hostList = list(host)

    #Code executes only if the first item in hostList is an alpha character
    if hostList[0].isalpha() != True:
        validHostname = False
    
    #Checks that the hostname is within acceptable range
    if len(hostList) <= 0 or len(hostList) >= 64:
        validHostname = False
    
    for char in hostList:

        #Check that each item in hostList is a letter, number, -, or _
        if char.isalnum() != True and char != "-":
            validHostname = False

    #hostname is set to lowercase in case user entered capitals
    host = host.lower()

    #Checks if hostname entered by user is already in the json file
    if host in file:
        validHostname = False
    return validHostname

#isHost verifies hostname is valid and that device is in device json
def isHost(host, file):
    
    validHost = True
    
    #Each letter of the hostname entered by the user is split into a list
    hostList = list(host)

    #Code executes only if the first item in hostList is an alpha character
    if hostList[0].isalpha() != True:
        validHost = False
    

    if len(hostList) <= 0 or len(hostList) >= 64:
        validHost = False
    
    for char in hostList:

        #Check that each item in hostList is a letter, number, -, or _
        if char.isalnum() != True and char != "-":
            validHost = False

    #hostname is set to lowercase in case user entered capitals
    host = host.lower()

    #Checks that device exists in the device json
    if host not in file:
        validHost = False
    return validHost

#addDev takes arguments for file to be edited, hostname, type, and ip address for the new device to add to the device json
def addDev(file, host, type, ip):

    #file is opened in read to obtain json data
    with open(file, 'r') as devDict:
        data = json.load(devDict)

    #Key of host with value of empty dictionary is created
    data[host] = {}
    with open(file, 'w') as devDict:
        json.dump(data, devDict)
    
    #Hostname, type, and ip are added into dictionary
    data[host]['hostname'] = host
    with open(file, 'w') as devDict:
        json.dump(data, devDict)
    data[host]['devicetype'] = type
    with open(file, 'w') as devDict:
        json.dump(data, devDict)
    data[host]['mgmtIP'] = ip
    with open(file, 'w') as devDict:
        json.dump(data, devDict)

#addHost takes arguments for file, hostname, and new hostname to change the hostname in the json file  
def addHost(file, host, host2):

    #file is opened in read to obtain json data
    with open(file, 'r') as devDict:
        data = json.load(devDict)

    #Hostname for device is updated to the new hostname entered by the user with the same dictionary values
    data[host2] = data.pop(host)
    with open(file, 'w') as devDict:
        json.dump(data, devDict)

    #hostname within dictionary value of host2 is updated to reflect the hostname change
    data[host2]['hostname'] = host2
    with open(file, 'w') as devDict:
        json.dump(data, devDict)

#addType takes file, host, and type as arguments to update the type for a device in the json file  
def addType(file, host, type):

    #file is opened in read to obtain json data
    with open(file, 'r') as devDict:
        data = json.load(devDict)

    #deviceType in json is updated to the new type entered by the user
    data[host]['devicetype'] = type
    with open(file, 'w') as devDict:
        json.dump(data, devDict)

#addMgmt takes file, host, and new IP entered by the user as arguments to update the ip for a device in the json file        
def addMgmt(file, host, ip):

    #file is opened in read to obtain json data
    with open(file, 'r') as devDict:
        data = json.load(devDict)

    #mgmtIp in json is updated to the new IP entered by the user
    data[host]['mgmtIP'] = ip
    with open(file, 'w') as devDict:
        json.dump(data, devDict)

#remDev takes arguments for file and device to remove a device from the json
def remDev(file, dev):

    #file is opened in read to obtain json data
    with open(file, 'r') as devDict:
        data = json.load(devDict)

    #deletes device from the json
    del data[dev]
    with open(file, 'w') as devDict:
        json.dump(data, devDict)

#choiceOne called if adding a new device to the json
def choiceOne():

    #modLoopOne is set to True for while loop and is broken if user chooses to exit or user completes prompts
    modLoopOne = True

    #user is prompted for device information such as type, hostname, and ip and all are checked to be valid
    while modLoopOne:
        userType = input('Enter the device type: ')
        print()
        if checkType(userType):
            newType = userType.upper()
            newHost = input('Enter the hostname: ')
            print()
            if validNewHost(newHost, savedList):
                newIp = input('Enter the management IP: ')
                print()
                if checkIp(newIp):

                    #Changes are displayed to the user and the user is prompted if they want to commit the changes
                    print('-' * 50)
                    print('Device with hostname: ' + newHost + ', type: ' + newType + ', and IP: ' + newIp + ' will be added.')
                    print('-' * 50)
                    print()
                    userVerify = input('Confirm changes? Y/N: ')
                    print()
                    userVerify = userVerify.lower()

                    #If user chooses to commit changes, the device is added to the json and the updated table is displayed
                    if userVerify == 'y':
                        addDev(fileLocation, newHost, newType, newIp)
                        printDev(getFile(fileLocation))
                        break
                    elif userVerify == 'n':
                        print('Changes will not be saved.')
                        break
                    else:
                        print('Only enter "y" for yes and "n" for no!')
                else:
                    print('IP address is not valid! \n')
            else:
                print('Hostname is not valid or is already in use \n')
        else:
            print('Only enter either "NXOS" or "IOSXE" for Type \n')

#choiceTwo called if modifying existing device in json
def choiceTwo():

    #modLoopTwo set to True for while loop and is broken if user chooses to exit or user completes prompts
    modLoopTwo = True

    #User is prompted to enter the hostname for the device to modify and then what they would like to modify for the device
    while modLoopTwo:
        modifyHost = input('Enter the full Hostname of the device you want to modify: ')
        print()

        #Contents of device are saved to be called on to verify devices exist before changing hostnames
        savedList = getDev(getFile(fileLocation))
        if isHost(modifyHost, savedList):

            #If device is in the json, user is prompted for what they would like to change for the device
            changeChoice = input('Enter 1 to change the Hostname, 2 to change the Device Type, 3 to change the Management IP, or 0 to exit: ')
            print()
            if changeChoice.isdigit():

                #If the user enters '1' they are prompted for a new hostname
                if changeChoice == '1':
                    newName = input('Enter the new hostname: ')
                    newName = newName.lower()
                    print()

                    #Hostname checked to be valid
                    if validNewHost(newName, savedList):

                        #Changes are displayed to the user and the user is prompted if they want to commit the changes
                        print('-' * 50)
                        print('Device hostname will be changed to: ' + newName)
                        print('-' * 50)
                        print()
                        userVerify = input('Confirm changes? Y/N: ')
                        print()
                        userVerify = userVerify.lower()

                        #If user chooses to commit changes, the hostname is changed and the updated table is displayed
                        if userVerify == 'y':
                            addHost(fileLocation, modifyHost, newName)
                            printDev(getFile(fileLocation))
                            break
                        elif userVerify == 'n':
                            print('Changes will not be saved.')
                            break
                        else:
                            print('Only enter "y" for yes and "n" for no!')
                    else:
                        print('Hostname is not valid or is already in use \n')

                #If user enters '2' they are prompted for a new type for the device
                elif changeChoice == '2':
                    userType = input('Enter the new device type: ')
                    print()

                    #Type entered by user is checked to be valid
                    if checkType(userType):
                        newType = userType.upper()

                        #Changes are displayed to the user and the user is prompted if they want to commit the changes
                        print('-' * 50)
                        print('Device type will be changed to: ' + newType)
                        print('-' * 50)
                        print()
                        userVerify = input('Confirm changes? Y/N: ')
                        userVerify = userVerify.lower()

                        #If user chooses to commit changes, the type is updated and the updated table is displayed
                        if userVerify == 'y':
                            addType(fileLocation, modifyHost, newType)
                            printDev(getFile(fileLocation))
                            break
                        elif userVerify == 'n':
                            print('Changes will not be saved.')
                            break
                        else:
                            print('Only enter "y" for yes and "n" for no!')
                    else:
                        print('Only enter "NXOS" or "IOSXE" for Type \n')

                #If user enters '3' they are prompted to enter a new management IP
                elif changeChoice == '3':
                    newIp = input('Enter the new management IP: ')
                    print()

                    #IP checked to be valid
                    if checkIp(newIp):

                        #Changes are displayed to the user and the user is prompted if they want to commit the changes
                        print('-' * 50)
                        print('Device IP will be changed to: ' + newIp)
                        print('-' * 50)
                        print()
                        userVerify = input('Confirm changes? Y/N: ')
                        userVerify = userVerify.lower()

                        #If user chooses to commit changes, the ip is updated and the updated table is displayed
                        if userVerify == 'y':
                            addMgmt(fileLocation, modifyHost, newIp)
                            printDev(getFile(fileLocation))
                            break
                        elif userVerify == 'n':
                            print('Changes will not be saved.')
                            break
                        else:
                            print('Only enter "y" for yes and "n" for no!')

                #If user enters '0' the loop is broken
                elif changeChoice == '0':
                    break
                else:
                    print('Only enter 1, 2, 3, or 0 \n')
            else:
                print('Only enter a number \n')
        else:
            print('Device does not exist! \n')

#choiceThree called if deleting device from json
def choiceThree():

    #modLoopThree set to True for while loop and is broken if user exits or 
    modLoopThree = True

    #User prompted for device to remove
    while modLoopThree:
        modifyHost = input('Enter the full Hostname of the device you want to delete: ')
        modifyHost = modifyHost.lower()
        print()

        #savedList contains current json data to check if device is in list before removing it
        savedList = getDev(getFile(fileLocation))
        if isHost(modifyHost, savedList):

            #Changes are displayed to the user and the user is prompted if they want to commit the changes
            print('-' * 50)
            print('Device ' + modifyHost + ' will be deleted')
            print('-' * 50)
            print()
            userVerify = input('Confirm changes? Y/N: ')
            print()
            userVerify = userVerify.lower()

            #If user chooses to commit changes, the device is removed and the updated table is displayed
            if userVerify == 'y':
                remDev(fileLocation, modifyHost)
                printDev(getFile(fileLocation))
                break
            elif userVerify == 'n':
                print('Changes will not be saved.')
                break
            else:
                print('Only enter "y" for yes and "n" for no!')
        else:
            print('Device does not exist! \n')
            print()

'''
BEGIN MAIN SCRIPT
'''

#fileLocation entered by the user and is used in all calls to read or write to the json
fileLocation = input('Enter the location for your Device JSON file: ')

#Table of devices in file is displayed
savedList = printDev(getFile(fileLocation))

#changingDev set to True for while loop and is broken if user types '0' to exit the program.
changingDev = True

#User is prompted to add, modify, delete, refresh table or exit. Functions are called depending on user's choice
while changingDev:
    modifyDev = input('Enter 1 to Add, 2 to Modify, 3 to Delete a device, 4 to refresh the device table, or 0 to exit: ')
    print()
    if modifyDev.isdigit():
        if modifyDev == '1':
            choiceOne()
        elif modifyDev == '2':
            choiceTwo()
        elif modifyDev == '3':
            choiceThree()
        elif modifyDev == '4':
            printDev(getFile(fileLocation))
        elif modifyDev == '0':
            exit()
        else:
            print('Only enter 1, 2, 3, or 0 \n')

    
    
    