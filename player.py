from character import Character
from room import Room
from item import Item

class Player(Character):
    """
    The user-controlled character, who can move through rooms,
    use items, pick up rewards, and engage in combat with monsters.
    """

    def __init__(self, name, description, hp, max_hp, attack_power):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.current_room = None
        self.storage = {} # list of class Item
        self.weight = 0
        self.max_weight = 64
        self.scannable = False # when true the player can read logs

    def set_current_room(self, room):
        """
        Set the room to the current room that the player is in.
        :param room: The room the player moves to.
        :return: None
        """
        self.current_room = room

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
            Pick up an item and add to storage, checking the weight limit before
            pick up.
        :param item: Item in which the player picks up.
        :return: True if the item has been picked up, otherwise False (too heavy).
        """

        if (self.weight + item.weight) > self.max_weight:
            return False
        self.storage[item.name] = item
        self.weight += item.weight
        return True

    def use(self, item):
        """
            Use a chosen item and.
        :param item: Item in which the player has in their backpack.
        """

    def show_storage(self):
        """
            Displays the storage.
        :return: The string content of the player's backpack.
        """
        if self.weight == 0:
            return "Your storage is empty."

        res = ["Your storage contains: \n"]
        for name, item in self.storage.items():
            res.append(f"- {name} (Weight: {item.weight})")
        res.append(f"\nCapacity: {self.weight}/{self.max_weight} bytes")
        return "\n".join(res)

    def remove_item(self, item_name):
        item_weight = self.storage[item_name].weight
        prev_weight = self.weight
        self.weight -= item_weight
        self.storage.pop(item_name)
        return f"You have removed {item_name} \nCapacity: {prev_weight} - {item_weight} --> {self.weight}/{self.max_weight} bytes"

    def is_alive(self):
        """
            Checks if the player's hp is 0.
        :return: True if player has hp > 0, False otherwise.
        """
        if self.hp == 0:
            return False
        else:
            return True




class NotInStorageError(Exception):
    """A custom exception to handle items not in backpack."""
    def __init__(self, item, message):
        print(f'{item} {message}')
