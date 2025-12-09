from item import Item

class Key(Item):
    def __init__(self, name, description, weight, key_id):
        super().__init__(self, name, description, weight)
        self.key_id = key_id