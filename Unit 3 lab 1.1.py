# ---------------------------------------------------------
#Name: Unit 3 Lab
#      
#Author:Tory Stietz    
# 
#Date created: 2/3/2021
# 
#Script Function1: Asks a user for their first and last name, saves first and last name as a variable.
#Script Function2: Have the script welcome them by replying "Welcome to Python, firstname. Lastname is a really interesting surname! Are you related to the famous Victoria lastname?”
# 
#Script References: W3schools.com/python
# 
#Special Instructions: Enter desired username when prompted to do so.
#
#****************************
def checkName(uName):
    uNameList = uName.split()
#uName is a passed as a string and the split method.
    if len(uNameList) == 2:
        return True
#if the name entered is consists of two names True will be returned. If not False will be returned.
    else:
        return False
#creates a function that asks the user to enter a username with two names.
validEntry = False

while validEntry == False:   

    userName = input("Enter username:")
    #print("Username is: " + username)

    if checkName(userName) == True:
        fullname = userName.split()
        print("Welcome to Python, " + fullname[0] + ". " + fullname[1] + " is a really interesting surname! Are you related to Victoria " + fullname[1] + "?") 
        validEntry = True
    else:
        print("enter the correct number of names. ")
    
    

print("All done!")


#ntpServer is a dictionary that contains keys labeled Server1,2, and 3. Also in the dictionary are values represented by the ip addresses.


ntpServer = {
    "ServerIP": "Addresses",
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6"

    }

print(ntpServer)


keystring = ""

for key in ntpServer.keys():
    print("key = " + key + " \t value = " + ntpServer[key])
    keystring = keystring + "\t" + key

#prints stars and returns no value
def printChar():
    print("*" + 50)

#validNum function

def validNum(number) :

    if number.isnumeric() == True :
        if int(number) >= 1 and int(number) <= 10 :
            return True
        else :
            return False





