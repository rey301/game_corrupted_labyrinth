from entity import Entity

class Item:
    def __init__(self, name, description, weight):
        super.__init__(name, description)
        self.weight = weight

    def user(self):
        """
            Uses the item's in-game effect (e.g. healing, remove corruption)
        :return: None
        """