from deck import Deck, DeckContainer
import requests

def valid_data_point(data):
    return "srPrice" in data and "urPrice" in data and "deckType" in data and "name" in data["deckType"] \
        and "main" in data and "extra" in data and "side" in data

def categorize_decks(decks):
    d = {}
    for deck in decks:
        container = d.setdefault(deck.name, DeckContainer(deck.name))
        container.add_deck(deck)
        
    return d


r = requests.get("https://www.masterduelmeta.com/api/v1/top-decks?created[$gte]=2024-03&created[$lt]=2024-04")
status_code = r.status_code
if status_code != 200:
    print("Get request unsuccessful with status code: {}".format(status_code))
    raise SystemExit

decks = []
text = r.json()
for data in text:
    if valid_data_point(data):
        d = Deck(data["deckType"]["name"], data["urPrice"], data["srPrice"],
                 data["main"], data["extra"], data["side"])
        decks.append(d)
    
containers = categorize_decks(decks)
sorted_containers = sorted(containers.values(), key=lambda x: x.get_avg_deck_cost(), reverse=True)
for container in sorted_containers:
    print(container.name, container.get_avg_deck_cost(), container.get_avg_deck_with_side_cost())

