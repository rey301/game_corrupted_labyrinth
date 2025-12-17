from entities.item import Item


class Med(Item):
    """
    Defines the heal item that the player can use to heal and raises their hp back to a certain level.
    """
    def __init__(self, name, description, weight, heal, uses, max_uses):
        super().__init__(name, description, weight)
        self.heal = heal
        self.uses = uses
        self.max_uses = max_uses

    def use(self, player):
        """
        Heals the player when used and doesn't over-heal if it goes over the player's max hp.
        :param player: The player that heals with the item.
        :return: The amount of hp recovered
        """
        prev_hp = player.hp
        # if a max heal item detected then heal player to maximum
        if self.heal == -1:
            player.hp = player.max_hp
        else:
            # heals player, but caps at max_hp using min()
            player.hp = min(player.max_hp, player.hp + self.heal)

        self.uses -= 1
        recover_amount = player.hp - prev_hp

        # determine if we keep the item
        status = "remove" if self.uses == 0 else "keep"

        msg = f"HP recovered: {prev_hp}+{recover_amount} --> {player.hp}/{player.max_hp}"
        return msg, status
