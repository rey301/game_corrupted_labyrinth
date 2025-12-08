from character import Character
from item import Item

class Monster:
    def __init__(self, hp, max_hp, attack_power, reward):
        super.__init__(hp, max_hp, attack_power)
        self.reward = reward