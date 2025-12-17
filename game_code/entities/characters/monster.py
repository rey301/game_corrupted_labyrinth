from game_code.entities.character import Character


class Monster(Character):
    """
    Monster character in the game;
    they can block exits and carry rewards for the player to pick up and use.
    """

    def __init__(self, name, description, hp, max_hp, attack_power, reward, blocks_exit=None):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.reward = reward
        self.blocks_exit = blocks_exit # the exit that the monster blocks
