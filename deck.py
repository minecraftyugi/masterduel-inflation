from datetime import datetime

class Deck:
    def __init__(self, name, ur_cost, sr_cost, main_deck, extra_deck, side_deck):
        self.name = name
        self.ur_cost = ur_cost
        self.sr_cost = sr_cost
        self.main_deck = main_deck
        self.extra_deck = extra_deck
        self.side_deck = side_deck
        self.deck_size = self._get_deck_size()

        self.total_urs = self.ur_cost // 30
        self.total_srs = self.sr_cost // 30
        self.total_others = self.deck_size - self.total_urs - self.total_srs

        # sr is 12x more likely than r/n, and ur is 3x more likely than sr
        self.other_weight = 1
        self.sr_weight = 12
        self.ur_weight = 36

    def _get_deck_size(self):
        deck_size = 0
        deck_size += self._get_cards_in_deck(self.main_deck)
        deck_size += self._get_cards_in_deck(self.extra_deck)
        deck_size += self._get_cards_in_deck(self.side_deck)
        return deck_size
    
    def _get_cards_in_deck(self, deck):
        cards = 0
        for card in deck:
            if "amount" in card:
                cards += card["amount"]

        return cards

    def get_cost(self):
        return self.total_urs * self.ur_weight + \
                self.total_srs + self.sr_weight + \
                self.total_others * self.other_weight
    
    def get_total_urs(self):
        return self.total_urs
    
    def get_total_srs(self):
        return self.total_srs
    
    def get_total_others(self):
        return self.total_others
        
class DeckContainer:
    def __init__(self, name, decks=[]):
        self.name = name
        self.decks = decks[:]
        self.decks_without_side = self._get_decks_without_side()

    def _get_decks_without_side(self):
        no_side_decks = []
        for deck in self.decks:
            if len(deck.side_deck) == 0:
                no_side_decks.append(deck)

        return no_side_decks

    def add_deck(self, deck):
        self.decks.append(deck)
        if len(deck.side_deck) == 0:
            self.decks_without_side.append(deck)

    def get_deck_size(self):
        return len(self.decks)

    def get_decks_without_side_size(self):
        return len(self.decks_without_side)

    def get_avg_deck_cost(self):
        if len(self.decks) == 0:
            return 0
        return sum(deck.get_cost() for deck in self.decks) / len(self.decks)

    def get_avg_deck_without_side_cost(self):
        if len(self.decks_without_side) == 0:
            return 0
        
        return sum(deck.get_cost() for deck in self.decks_without_side) / len(self.decks_without_side)
    
    def get_avg_total_urs(self):
        if len(self.decks) == 0:
            return 0
        
        return sum(deck.get_total_urs() for deck in self.decks) / len(self.decks)
    
    def get_avg_total_srs(self):
        if len(self.decks) == 0:
            return 0
        
        return sum(deck.get_total_srs() for deck in self.decks) / len(self.decks)
    
    def get_avg_total_others(self):
        if len(self.decks) == 0:
            return 0
        
        return sum(deck.get_total_others() for deck in self.decks) / len(self.decks)
    
class TimeIntervalDeckContainers:
    def __init__(self, start_date, end_date, deck_containers) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.deck_containers = deck_containers[:]

    def sort(self):
        self.deck_containers.sort(key=lambda x: x.get_deck_size(), reverse=True)

    def get_avg_cost(self, relevant_deck_count):
        self.sort()
        total_cost = 0
        total_decks = 0
        for i in range(min(relevant_deck_count, len(self.deck_containers))):
            deck_size = self.deck_containers[i].get_deck_size()
            total_cost += self.deck_containers[i].get_avg_deck_cost() * deck_size
            total_decks += deck_size

        return total_cost / total_decks
    
    def get_avg_total_urs(self, relevant_deck_count):
        self.sort()
        total_urs = 0
        total_decks = 0
        for i in range(min(relevant_deck_count, len(self.deck_containers))):
            deck_size = self.deck_containers[i].get_deck_size()
            total_urs += self.deck_containers[i].get_avg_total_urs() * deck_size
            total_decks += deck_size

        return total_urs / total_decks
    
    def get_avg_total_srs(self, relevant_deck_count):
        self.sort()
        total_srs = 0
        total_decks = 0
        for i in range(min(relevant_deck_count, len(self.deck_containers))):
            deck_size = self.deck_containers[i].get_deck_size()
            total_srs += self.deck_containers[i].get_avg_total_srs()
            total_decks += deck_size

        return total_srs / total_decks
    
    def get_avg_total_others(self, relevant_deck_count):
        self.sort()
        total_others = 0
        total_decks = 0
        for i in range(min(relevant_deck_count, len(self.deck_containers))):
            deck_size = self.deck_containers[i].get_deck_size()
            total_others += self.deck_containers[i].get_avg_total_others() * deck_size
            total_decks += deck_size

        return total_others / total_decks
    
    def get_human_readable_start_date(self):
        date_format = "%Y-%m"
        date_obj = datetime.strptime(self.start_date, date_format)
        return date_obj.strftime("%b %Y")
    
    def get_human_readable_end_date(self):
        date_format = "%Y-%m"
        date_obj = datetime.strptime(self.end_date, date_format)
        return date_obj.strftime("%b %Y")