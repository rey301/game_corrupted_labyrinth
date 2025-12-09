from item import Item

class Consumable(Item):
    def __init__(self, name, description, weight, heal):
        super().__init__(name, description, weight)
        self.heal = heal

    def use(self, player):
        prev_hp = player.hp
        player.hp += self.heal
        return f"HP recovered: {prev_hp}+{self.heal} --> {player.hp}"

