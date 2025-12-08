from entity import Entity

class Item:
    def __init__(self, name, description, weight, corrupted):
        super.__init__(name, description)
        self.weight = weight
        self.corrupted = corrupted

    def user(self):
        """
            Uses the item's in-game effect (e.g. healing, remove corruption)
        :return: None
        """