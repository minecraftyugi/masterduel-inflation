from card import Card
from json import JSONEncoder
import json, requests

DECK_URL = "https://www.masterduelmeta.com/api/v1/top-decks"
CARD_URL = "https://www.masterduelmeta.com/api/v1/cards"
CARD_LIMIT = 2500

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__ 

def get_deck_data(start_date, end_date):
    payload = {"created[$gte]": start_date,
               "created[$lt]": end_date,
               "limit": 0}
    r = requests.get(DECK_URL, params=payload)
    status_code = r.status_code
    if status_code != 200:
        print("Get request for top decks unsuccessful with status code: {}".format(status_code))
        raise SystemExit

    return r.json()

def get_card_data(limit, page_num):
    payload = {"cardSort": "popRank",
               "aggregate": "search",
               "limit": limit,
               "page": page_num}
    r = requests.get(CARD_URL, params=payload)
    status_code = r.status_code
    if status_code != 200:
        print("Get request for cards unsuccessful with status code: {}".format(status_code))
        raise SystemExit

    return r.json()

def get_all_cards():
    under_limit = False
    i = 0
    cards = {}
    while not under_limit:
        print(i)
        card_data = get_card_data(CARD_LIMIT, i)
        for data in card_data:
            rarity = data.get("rarity", None)
            c = Card(data["_id"], data["name"], rarity)
            cards[c.id] = c

        under_limit = len(card_data) < CARD_LIMIT
        i += 1

    return cards

f = open("cards.json", "w", encoding="utf8")
cards = get_all_cards()
json.dump(cards, f, cls=Encoder)
f.close()