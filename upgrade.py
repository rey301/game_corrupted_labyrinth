from item import Item

class Upgrade(Item):
    def __init__(self, name, description, weight, upgrade_type):
        super().__init__(name, description, weight)
        self.upgrade_type = upgrade_type

    def use(self, player=None, room=None, world=None):
        """
        When certain items are used, it causes something to happen in the world, or to the player (e.g.
        reading logs).
        :param player: The player that is currently in the game.
        :param room: The room that the player is currently in.
        :param world: The world with attributes of the game.
        :return: The text that will be printed to the user, and the flag if the item gets removed.
        """
        room = player.current_room
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






