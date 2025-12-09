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

    def take_damage(self, amount):
        """
            Reduce the amount of hp by a given amount.
        :param amount: Damage dealt.
        :return: None
        """

    def attack(self, target):
        """
            Perform attack on another character.
        :param target: The character being attacked.
        """
