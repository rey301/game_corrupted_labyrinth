"""
Create a room described "description". Initially, it has no exits. The
'description' is something like 'kitchen' or 'an open court yard'.
"""

from entity import Entity
from item import Item

class Room(Entity):
    """A room in the game."""

    def __init__(self, name, description, monster=None, puzzle=None):
        """
            Constructor method.
        :param monster:
        """
        super().__init__(name, description)
        self.exits = {}  # Dictionary of Room objects
        self.items = [] # List of items in the current room
        self.monster = monster # Current monster in the room
        self.puzzle = puzzle

    def set_exit(self, dir, room):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room).
        :param dir: The direction leading out of this room.
        :param room: The room that this direction takes you to.
        :return: None
        """
        self.exits[dir] = room

    def add_item(self, item):
        """
            Adds an item to the room.
        :param item: The item that is added to the room.
        :return: None
        """
        self.items.append(item)

    def describe(self):
        """
            Returns description of the room (including items and exits).
        :return: Description string.
        """
        return self.description