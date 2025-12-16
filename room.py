"""
Create a room described "description". Initially, it has no exits. The
'description' is something like 'kitchen' or 'an open court yard'.
"""

from entity import Entity

class Room(Entity):
    """A room in the game."""

    def __init__(self, name, description, locked=False, puzzle=None):
        """
            Constructor method.
        :param monster:
        """
        super().__init__(name, description)
        self.locked = locked
        self.hidden_path = False # for hidden room
        self.exits = {}  # Dictionary of Room objects
        self.items = {} # List of items in the current room
        self.monsters = {} # monsters in the current room
        self.puzzle = puzzle
        self.locked_exits = {} # exits that are locked from the player
        self.kernel_unlock = False

    def set_exit(self, dir, room):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room).
        :param dir: The direction leading out of this room.
        :param room: The room that this direction takes you to.
        :return: None
        """
        self.exits[dir] = room

    def get_exit(self, dir):
        return self.exits[dir]

    def add_item(self, item):
        """
            Adds an item to the room.
        :param item: The item that is added to the room.
        :return: None
        """
        self.items[item.name] = item

    def remove_item(self, item):
        """
        Removes an item from the room.
        :param item: The item that is removed fromthe room
        :return: None
        """
        self.items.pop(item.name)

    def remove_puzzle(self):
        """
        Removes puzzle from the room.
        :param puzzle: The puzzle that is removed from the room.
        :return: None
        """
        self.puzzle = None

    def add_monster(self, monster):
        """
            Adds a new monster to the room.
        :param monster: The Monster that is added.
        :return: None
        """
        self.monsters[monster.name] = monster

    def remove_monster(self, monster):
        self.monsters.pop(monster.name)

    def describe(self):
        """
        Returns description of the room (including items and exits).
        :return: Description string.
        """
        return self.description

    def lock_exit(self, direction, lock_id):
        self.locked_exits[direction] = lock_id

    def unlock_exit(self, direction):
        if direction in self.locked_exits:
            self.locked_exits.pop(direction)

    def update_description(self, new_desc):
        self.description = new_desc

class DirectionNotValidError(Exception):
    def __init__(self, message):
        print(message)
