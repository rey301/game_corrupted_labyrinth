from item import Item

class Lore(Item):
    def __init__(self, name, description, weight, content, req_scanner=False):
        super().__init__(name, description, weight)
        self.content = content

    def use(self, player=None, room=None, world=None):
        if not player.scannable:
            return "You need to activate the scanner module to decrypt the logs.", "keep"
        return self.content, "keep"