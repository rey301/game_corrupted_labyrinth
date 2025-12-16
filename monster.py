from character import Character

class Monster(Character):
    def __init__(self, name, description, hp, max_hp, attack_power, reward, blocks_exit=None):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.reward = reward
        self.blocks_exit = blocks_exit