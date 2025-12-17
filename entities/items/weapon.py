from entities.item import Item

class Weapon(Item):
    """
    Defines weapons that the player can use in the game against monsters.
    """
    def __init__(self, name, description, weight, damage):
        super().__init__(name, description, weight)
        self.damage = damage
