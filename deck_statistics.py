MIN_DECK_CONTAINER_SIZE = 13
RELEVANT_DECKS = 10

class DeckStatistics:
    def __init__(self, deck_containers, relevant_decks=RELEVANT_DECKS):
        self.time_interval_deck_containers = deck_containers[:]
        self.relevant_decks = relevant_decks
        self._sort_deck_containers()
        if len(self.time_interval_deck_containers) < MIN_DECK_CONTAINER_SIZE:
            print("Too few time interval deck containers")
            raise SystemExit

    def _sort_deck_containers(self):
        for i in range(len(self.time_interval_deck_containers)):
            container = self.time_interval_deck_containers[i]
            container.sort()

    def get_monthly_inflation(self):
        return self.time_interval_deck_containers[0].get_avg_cost(self.relevant_decks) / self.time_interval_deck_containers[1].get_avg_cost(self.relevant_decks)
    
    def get_yearly_inflation(self):
        return self.time_interval_deck_containers[0].get_avg_cost(self.relevant_decks) / self.time_interval_deck_containers[12].get_avg_cost(self.relevant_decks)
    
    def get_total_inflation(self):
        return self.time_interval_deck_containers[0].get_avg_cost(self.relevant_decks) / self.time_interval_deck_containers[-1].get_avg_cost(self.relevant_decks)