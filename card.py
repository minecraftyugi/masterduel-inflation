class Card:
    def __init__(self, id, name, rarity, weight=1):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.weight = weight

    def __str__(self) -> str:
        return "Card [Id: {} Name: {} Rarity: {} Weight: {}]".format(self.id, self.name, self.rarity, self.weight)

    def set_weight(self, weight):
        self.weight = weight
