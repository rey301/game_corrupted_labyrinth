from character import Character
from room import Room
from item import Item

class Player(Character):
    """
    The user-controlled character, who can move through rooms,
    use items, pick up rewards, and engage in combat with monsters.
    """

    def __init__(self, hp, max_hp, attack_power, room):
        super().__init__(hp, max_hp, attack_power)
        self.current_room = room
        self.backpack = [] # list of class Item
        self.max_weight = 0

    def move(self, direction):
        """
            Attempt to move player in a new room in direction chosen.
            If the exit exists, the player's current room is updated.
            If no exit exists and error message is shown.
        :param direction: Direction in which the player moves.
        :return: True if dir is a valid move (room is changed), otherwise False (no exit).
        """


    def pick_up(self, item):
        """
            Pick up an item and add to backpack, checking the weight limit before
            pick up.
        :param item: Item in which the player picks up.
        :return: True if the item has been picked up, otherwise False (too heavy).
        """

    def use(self, item):
        """
            Use a chosen item and.
        :param item: Item in which the player has in their backpack.
        """

    def show_backpack(self):
        """
            Displays the backpack contents
        :return: The string content of the player's backpack.
        """

    def is_alive(self):
        """
            Checks if the player's hp is 0.
        :return: True if player has hp > 0, False otherwise.
        """
        if self.hp == 0:
            return False
        else
            return True



class NotInBackpackError(Exception):
    """A custom exception to handle items not in backpack."""
    def __init__(self, item, message):
        print(f'{item} {message}')
