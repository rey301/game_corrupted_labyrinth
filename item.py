from entity import Entity

class Item(Entity):
    def __init__(self, name, description, weight):
        super().__init__(name, description)
        self.weight = weight

    def use(self, player=None, room=None, world=None):
        """
            Base method for using an item, where subclasses override as needed.
        :return: The message and flag to keep or drop the item.
        """
        return "Nothing happens.", "keep"