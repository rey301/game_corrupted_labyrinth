"""
Backpack module for carrying items.
"""


class Backpack:
    """
    A class to allow us to pickup and put down items...
    Backpack is limited to number of items set by capacity.
    This example incorporates a user defined exception.
    """

    def __init__(self, capacity):
        self.contents = []
        self.capacity = capacity

    def add_item(self, item):
        """Adds an item to our backpack."""
        if len(self.contents) < self.capacity:
            self.contents.append(item)
            return True
        return False

    def remove_item(self, item):
        """Removes an item from our backpack."""
        try:
            if item not in self.contents:
                raise NotInBackpackError(item, 'is not in the backpack.')
            self.contents.remove(item)
        except NotInBackpackError:
            print('Exception handled here...')
        finally:
            print('Carrying on...')

    def check_item(self, item):
        """Returns True if item is in backpack, False otherwise."""
        return item in self.contents


class NotInBackpackError(Exception):
    """A custom exception to handle items not in backpack."""
    def __init__(self, item, message):
        print(f'{item} {message}')
