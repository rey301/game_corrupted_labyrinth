from entity import Entity

class Character(Entity):
    def __init__(self, name, description, hp, max_hp, attack_power):
        super().__init__(name, description)
        self.hp = hp
        self.max_hp = max_hp
        self.attack_power = attack_power

    def is_alive(self):
        """
            Returns whether the character's hp is < 0
        :return: True if character's hp is > 0, False otherwise.
        """
        return self.hp > 0

    def attack(self, target):
        """
            Perform attack on another character.
        :param target: The character being attacked.
        :return: Damage dealt as an integer
        """
        damage_dealt = self.attack_power
        prev_hp = target.hp
        target.hp -= damage_dealt
        if target.hp < 0:
            damage_dealt = prev_hp
            target.hp = 0
        return damage_dealt