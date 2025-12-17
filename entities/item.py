from entities.entity import Entity


class Item(Entity):
    """
    An item in the world with a specific weight,
    where the use method is overridden by a specified item type.
    """

    def __init__(self, name, description, weight):
        super().__init__(name, description)
        self.weight = weight

    def use(self, player):
        """
            Base method for using an item, where subclasses override as needed.
        :return: The message and flag to keep or drop the item.
        """
        return "Nothing happens.", "keep"
