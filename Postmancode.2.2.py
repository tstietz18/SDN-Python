import requests

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" #shuffle

payload={}
headers = {
  'Cookie': '__cfduid=d54398e903fbf4ce072c877921545ae511613002800'
}

response = requests.request("GET", url, headers=headers, data=payload)



cardDeck = response.json()


deck_id = cardDeck["deck_id"]

NumberOfCards = input("How many cards do you want to draw?") 

url = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" +  NumberOfCards

payload={}
headers = {
  'Cookie': '__cfduid=d54398e903fbf4ce072c877921545ae511613002800'
}

response = requests.request("GET", url, headers=headers, data=payload)

CardsDrawn = response.json()

print(CardsDrawn)

for card in CardsDrawn["cards"]:
    print(card)

for card in CardsDrawn["cards"]:
    print(card["value"] + " of " + card["suit"])

    
