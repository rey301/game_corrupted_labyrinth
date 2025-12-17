from game_code.entities.entity import Entity


class Room(Entity):
    """
    A room in the game which contains monsters, items, puzzles, and locked exits.
    """

    def __init__(self, name, description, locked=False, puzzle=None):
        super().__init__(name, description)
        self.locked = locked
        self.exits = {}  # Dictionary of Room entities
        self.items = {}  # List of items in the current room
        self.monsters = {}  # monsters in the current room
        self.puzzle = puzzle
        self.locked_exits = {}  # exits that are locked from the player
        self.kernel_unlock = False  # this check is for the last room

    def set_exit(self, direction, room):
        """
        Adds an exit for a room. The exit is stored as a dictionary
        entry of the (key, value) pair (direction, room).
        :param direction: The direction leading out of this room.
        :param room: The room that this direction takes you to.
        :return: None
        """
        self.exits[direction] = room

    def get_exit(self, direction):
        return self.exits[direction]

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
        :param item: The item that is removed from the room.
        :return: None
        """
        self.items.pop(item.name)

    def remove_puzzle(self):
        """
        Removes puzzle from the room.
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
        """
        Removes a monster from the room.
        :param monster: The monster that is removed.
        :return: None
        """
        self.monsters.pop(monster.name)

    def describe(self):
        """
        Returns description of the room (including items and exits).
        :return: Description string.
        """
        return self.description

    def lock_exit(self, direction, lock_id):
        """
        Adds a locked exit in the locked_exit dictionary and this blocks the player
        from moving towards a certain direction.
        :param direction: The direction that is locked.
        :param lock_id: The lock_id needed to unlock that exit.
        :return: None
        """
        self.locked_exits[direction] = lock_id

    def unlock_exit(self, direction):
        """
        Unlock the exit in the certain direction where that direction must be in the locked_exits dictionary.
        :param direction: The direction of the exit that is unlocked.
        :return: None
        """
        if direction in self.locked_exits:
            self.locked_exits.pop(direction)

    def update_description(self, new_desc):
        """
        Replaces the description of the room.
        :param new_desc: The new description that replaces the current one.
        :return: None
        """
        self.description = new_desc

