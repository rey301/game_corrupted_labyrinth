from item import Item

class Consumable(Item):
    def __init__(self, name, description, weight, heal):
        super().__init__(self, name, description, weight)
        self.heal = heal
