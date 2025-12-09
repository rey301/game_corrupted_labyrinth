from item import Item

class Misc(Item):
    def __init__(self, name, description, weight, misc_id):
        super().__init__(self, name, description, weight)
        self.misc_id = misc_id