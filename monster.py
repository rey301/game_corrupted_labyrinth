from character import Character
from item import Item

class Monster(Character):
    def __init__(self, name, description, hp, max_hp, attack_power, reward):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.reward = reward