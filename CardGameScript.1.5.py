# ---------------------------------------------------------
#Name: CardGameScript.1
#      
#Author: Tory Stietz    
# 
#Date created: 3/2/2021
# 
#Script Function: 
# 
#Script References:
# 
#Special Instructions:
#
#****************************

import requests
import json


def count_cards(CardsDrawn):
    CardValues = {
    "Ace" : 1,
    "King" : 10,
    "Queen" : 10,
    "Jack" : 10
    }
    print("We are in the function \t")
    print(CardsDrawn['cards'])
    print()
    print()
    score = 0
    for card in CardsDrawn['cards']:
       print(card['value'])
       #if card['value'].isdigit() == True:
       if card['Ace'].isdigit() == True:
           print(card['Ace'])
       if card['King'].isdigit() == True:
           print(card['King'])
       if card['Queen'].isdigit() == True:
           print(card['Queen'])
       if card['Jack'].isdigit() == True:
            print(card['Jack'])
           
    #elif card['value'].isdigit == False:
     #   print("enter a valid digit")

    return humanScore

def drawCards(deck_id,NumberOfCards):
    url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" +  NumberOfCards

    payload={}
    headers = {
      'Cookie': '__cfduid=d54398e903fbf4ce072c877921545ae511613002800'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    CardsDrawn = response.json()
    return CardsDrawn

# this section shuffles the deck
url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" #shuffle

payload={}
headers = {
  'Cookie': '__cfduid=d54398e903fbf4ce072c877921545ae511613002800'
}

response = requests.request("GET", url, headers=headers, data=payload)

cardDeck = response.json()
#***********************************************



deck_id = cardDeck["deck_id"]

NumberOfCards = input("How many cards do you want to draw?") 

CardsDrawn = drawCards(deck_id,NumberOfCards)

humanScore = count_cards(CardsDrawn)

#print(CardsDrawn)
print(humanScore)

CardsDrawn = drawCards(deck_id,NumberOfCards)

computerScore = count_cards(CardsDrawn)

print(computerScore)

if humanScore > computerScore:
    print("Human Wins!!")

else:
    print("Computer Wins!!")

if humanScore == computerScore:
    print("it's a tie!!")



##for card in CardsDrawn["cards"]:
##    print(card)
##
##for card in CardsDrawn["cards"]:
##    print(card["value"] + " of " + card["suit"])
##
### this section shuffles the deck
##url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" #shuffle
##
##payload={}
##headers = {
##  'Cookie': '__cfduid=d54398e903fbf4ce072c877921545ae511613002800'
##}
##
##response = requests.request("GET", url, headers=headers, data=payload)
##
##cardDeck = response.json()
###***********************************************
##def validNum(NumOfCards) :
##
##    if number.isnumeric() == True :
##        if int(NumOfCards) >= 0 and int(NumOfCards) <= 5:
##            return True
##        else : False
##
##ComputerCards = input("Draw this many cards." + 5)
##print(ComputerCards)
##
###print(" I drew a"_____ " of " ______ " and a " ________ " of " ______)
##



        
# end of script
