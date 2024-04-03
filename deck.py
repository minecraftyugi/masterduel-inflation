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
        return total_urs * self.ur_weight + total_srs + self.sr_weight + total_other_rarities * self.other_weight
        
class DeckContainer:
    def __init__(self, name, decks=[]):
        self.name = name
        self.decks = decks[:]
        self.decks_with_side = self._get_decks_with_side()

    def _get_decks_with_side(self):
        side_decks = []
        for deck in self.decks:
            if len(deck.side_deck) > 0:
                side_decks.append(deck)

        return side_decks

    def add_deck(self, deck):
        self.decks.append(deck)
        if len(deck.side_deck) > 0:
            self.decks_with_side.append(deck)

    def get_avg_deck_cost(self):
        if len(self.decks) == 0:
            return 0
        return sum(deck.get_cost() for deck in self.decks) / len(self.decks)

    def get_avg_deck_with_side_cost(self):
        if len(self.decks_with_side) == 0:
            return 0
        
        return sum(deck.get_cost() for deck in self.decks_with_side) / len(self.decks_with_side)
    
