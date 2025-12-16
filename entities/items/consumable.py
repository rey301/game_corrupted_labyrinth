from entities.item import Item

class Consumable(Item):
    def __init__(self, name, description, weight, heal, uses, max_uses):
        super().__init__(name, description, weight)
        self.heal = heal
        self.uses = uses
        self.max_uses = max_uses

    def use(self, player=None, room=None, world=None):
        """
        Heals the player when used and doesn't overheal if it goes over the player's max hp.
        :param player: The player in the game.
        :param room: The current room the player is in.
        :param world: The world that the player is in.
        :return: The amount of hp recovered
        """



        prev_hp = player.hp
        # if a max heal item detected then heal player to maximum
        if self.heal == -1:
            player.hp = player.max_hp
        else:
            # Heals player, but caps at max_hp using min()
            player.hp = min(player.max_hp, player.hp + self.heal)

        self.uses -= 1
        recover_amount = player.hp - prev_hp

        # Determine if we keep the item
        status = "remove" if self.uses == 0 else "keep"

        msg = f"HP recovered: {prev_hp}+{recover_amount} --> {player.hp}/{player.max_hp}"
        return msg, status
