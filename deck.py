class Deck:
    def __init__(self, name, ur_cost, sr_cost, main_deck, extra_deck, side_deck):
        self.name = name
        self.ur_cost = ur_cost
        self.sr_cost = sr_cost
        self.main_deck = main_deck
        self.extra_deck = extra_deck
        self.side_deck = side_deck
        self.deck_size = len(main_deck) + len(extra_deck) + len(side_deck)

        # sr is 12x more likely than r/n, and ur is 3x more likely than sr
        self.other_weight = 1
        self.sr_weight = 12
        self.ur_weight = 36

    def get_cost(self):
        total_urs = self.ur_cost // 3
        total_srs = self.sr_cost // 3
        total_other_rarities = self.deck_size - total_urs - total_srs
        return total_urs * self.ur_weight + \
                total_srs + self.sr_weight + \
                total_other_rarities * self.other_weight
        
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