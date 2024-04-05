from deck import Deck, DeckContainer, TimeIntervalDeckContainers
from deck_statistics import DeckStatistics
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

BASE_URL = "https://www.masterduelmeta.com/api/v1/top-decks"

def get_data(start_date, end_date):
    payload = {"created[$gte]": start_date,
               "created[$lt]": end_date,
               "limit": 0}
    r = requests.get(BASE_URL, params=payload)
    status_code = r.status_code
    if status_code != 200:
        print("Get request unsuccessful with status code: {}".format(status_code))
        raise SystemExit

    return r.json()
    

def valid_data_point(data):
    return "srPrice" in data and "urPrice" in data and "deckType" in data and "name" in data["deckType"] \
        and "main" in data and "extra" in data and "side" in data

def categorize_decks(decks):
    d = {}
    for deck in decks:
        container = d.setdefault(deck.name, DeckContainer(deck.name))
        container.add_deck(deck)
        
    return d

def get_month_with_offset(offset):
    now = datetime.now()
    past = now - relativedelta(months=offset)
    return past.strftime("%Y-%m")

time_interval_containers = []
for i in range(26):
    start_time = get_month_with_offset(i+1)
    end_time = get_month_with_offset(i)
    print()
    print(start_time)

    decks = []
    text = get_data(start_time, end_time)
    for data in text:
        if valid_data_point(data):
            d = Deck(data["deckType"]["name"], data["urPrice"], data["srPrice"],
                    data["main"], data["extra"], data["side"])
            decks.append(d)
        
    containers = categorize_decks(decks)
    sorted_containers = sorted(containers.values(), key=lambda x: x.get_deck_size(), reverse=True)
    for container in sorted_containers:
        print(container.name, container.get_deck_size(),
            container.get_avg_deck_cost(), container.get_avg_deck_without_side_cost())
        
    time_interval_containers.append(TimeIntervalDeckContainers(start_time, end_time, sorted_containers))

deck_stats = DeckStatistics(time_interval_containers)
print(deck_stats.get_monthly_inflation())
print(deck_stats.get_yearly_inflation())
print(deck_stats.get_total_inflation())