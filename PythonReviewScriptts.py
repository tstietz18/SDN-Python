# ---------------------------------------------------------
#Name: Python Review1
#      
#Author:Tory Stietz    
# 
#Date created: 1/27/21
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
    if len(uNameList) == 2:
        return True
    else:
        return False

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








