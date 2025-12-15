from item import Item

class Consumable(Item):
    def __init__(self, name, description, weight, heal, uses, max_uses):
        super().__init__(name, description, weight)
        self.heal = heal
        self.uses = uses
        self.max_uses = max_uses

    def use(self, player, room=None, world=None):
        """
        Heals the player when used and doesn't overheal if it goes over the player's max hp.
        :param player: The player in the game.
        :param room: The current room the player is in.
        :param world: The world that the player is in.
        :return: The amount of hp recovered
        """
        prev_hp = player.hp
        player.hp += self.heal
        self.uses -= 1
        # if overheal just set the player's health to the max hp
        if player.hp > player.max_hp:
            player.hp = player.max_hp
            if self.uses == 0:
                return f"HP recovered: {prev_hp}+{self.heal} (Overhealed) --> {player.hp}/{player.max_hp}", "remove"
            else:
                return f"HP recovered: {prev_hp}+{self.heal} (Overhealed) --> {player.hp}/{player.max_hp}", "keep"
        else:
            if self.uses == 0:
                return f"HP recovered: {prev_hp}+{self.heal} --> {player.hp}/{player.max_hp}", "remove"
            else:
                return f"HP recovered: {prev_hp}+{self.heal} --> {player.hp}/{player.max_hp}", "keep"

