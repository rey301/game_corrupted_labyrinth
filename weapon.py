from item import Item

class Weapon(Item):
    def __init__(self, name, description, weight, damage):
        super().__init__(self, name, description, weight)
        self.damage = damage
