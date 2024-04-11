from deck import Deck, DeckContainer, TimeIntervalDeckContainers
from deck_statistics import DeckStatistics
from datetime import datetime
from dateutil.relativedelta import relativedelta
from inflation_charts import BarChart, LineChart, percent_format
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
for i in range(24):
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
    count = 0
    for container in sorted_containers:
        stats = f"Deck Name: {container.name} Deck Submissions: {container.get_deck_size()} " + \
                f"Avg Cost: {container.get_avg_deck_cost()} URs: {container.get_avg_total_urs()} " + \
                f"SRs: {container.get_avg_total_srs()} " + \
                f"N/Rs: {container.get_avg_total_others()}"
        stats = f"{container.name},{container.get_deck_size()}," + \
                f"{container.get_avg_deck_cost()},{container.get_avg_total_urs()}," + \
                f"{container.get_avg_total_srs()}," + \
                f"{container.get_avg_total_others()}"
        if count < 10:
            print(stats)
            count += 1
        
    time_interval_containers.append(TimeIntervalDeckContainers(start_time, end_time, sorted_containers))

deck_stats = DeckStatistics(time_interval_containers)
print("Monthly Inflation", percent_format(deck_stats.get_monthly_inflation()))
print("Yearly Inflation", percent_format(deck_stats.get_yearly_inflation()))


chart = BarChart(deck_stats)
chart.draw()

chart2 = LineChart(deck_stats)
chart2.draw()