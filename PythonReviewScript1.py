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
username = input("Enter username:")
print("Username is: " + username)


#user = "Tory Stietz"
#password =cisco

txt = ("Welcome to Python, Tory. Stietz is a really interesting surname! Are you related to Victoria Stietz?")
Intro = txt.split(", ")

print(Intro)


# split command is used to achieve proper spacing.

Name = 2
while Name < 3:
    Name += 1
    if Name == 3:

        print(Name)
# while loop is used to verify number of names allowed before an error message is received.        

mylist = "Tory, Stietz"
Name = len(mylist)

# list and len function are used to display instances when user name is present above.

# end of script
