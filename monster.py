from item import Item
from character import Character

class Monster:
    def __init__(self, reward, hp, max_hp, attack_power):
        super.__init__(hp, max_hp, attack_power)
        self.reward = reward