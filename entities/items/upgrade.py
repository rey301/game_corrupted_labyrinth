from entities.item import Item

class Upgrade(Item):
    """
    Defines upgrades in the game that can enhance a players stats or change a certain state.
    This includes upgrading their HP and storage, as well as allowing the player to read logs.
    """
    def __init__(self, name, description, weight, upgrade_type):
        super().__init__(name, description, weight)
        self.upgrade_type = upgrade_type

    def use(self, player):
        """
        When used a certain stat is upgraded or allowing the user to read logs.
        :param player: The player that is using the item.
        :return: The string message the is shown to the user, showing updates on their stats or state change.
        """

        # for expanding storage
        if self.upgrade_type == "storage":
            prev_max = player.max_weight
            player.max_weight += 32
            return f"System Upgraded: STORAGE \n{prev_max}+32 --> {player.max_weight}", "remove"

        # for increasing maximum health
        elif self.upgrade_type == "health":
            prev_max_hp = player.max_hp
            player.max_hp += 300
            player.hp = player.max_hp
            return f"System Upgraded: MAX HP \n{prev_max_hp}+300 --> {player.max_hp}", "remove"

        # for being able to read logs
        elif self.upgrade_type == "scan":
            player.scannable = True
            return f"Scan module activated. You are now able to read logs.", "remove"

        return "Nothing happens."






