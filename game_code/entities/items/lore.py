from game_code.entities.item import Item

class Lore(Item):
    """
    Log files in the game that reveals lore about the story.
    """
    def __init__(self, name, description, weight, content, req_scanner=False):
        super().__init__(name, description, weight)
        self.content = content

    def use(self, player):
        """
        Onced used, it checks if the scan module was activated, otherwise it can't use it.
        :param player: The player that uses the Lore item.
        :return: The string message for whether the player can read the log; if they can then
        it's the content that is returned.
        """
        if not player.scannable:
            return "You need to activate the scanner module to decrypt the logs.", "keep"
        return self.content, "keep"