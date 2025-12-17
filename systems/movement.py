import time
from entities.items.key import Key


class Movement:
    """
    Movement system for players in the game space. This checks for locked exits and blocked exits when moving.
    """

    def __init__(self, ui, game):
        self.ui = ui
        self.game = game

    def try_move(self, player, direction):
        """
        The player tries to move in a certain direction, and checks if a monster blocks or the exit is locked.
        :param player: The player that moves.
        :param direction: The direction in which the player tries to move.
        :return: True if the player is able to move in that direction, False otherwise.
        """
        room = player.current_room
        self.ui.display_text(f"Moving {direction}...")
        time.sleep(0.5)
        if direction not in room.exits:
            self.ui.display_text("You can't go that way!")
            return False

        next_room = room.get_exit(direction)

        if self.check_monster_block(direction):
            return False

        if self.check_locked_exit(direction, next_room):
            return False

        player.current_room = room.get_exit(direction)
        return True

    def check_monster_block(self, direction):
        """
        Check if a monster is blocking the exit.
        :param direction: The direction in which the monster is blocking.
        """
        room = self.game.player.current_room
        for monster in room.monsters.values():
            if monster.blocks_exit == direction:
                self.ui.clear_logs()
                self.ui.display_text(f"{monster.name} has blocked you!")
                self.ui.display_text("Defeating it is the only way in...")
                time.sleep(1)
                self.ui.display_text("")
                self.game.do_fight(monster.name)
                return True
        return False

    def check_locked_exit(self, direction, next_room):
        """
        Check if exit is locked and handle unlocking.
        :return: True if the exit is locked, False otherwise.
        """
        room = self.game.player.current_room

        if direction not in room.locked_exits:
            return False

        lock_id = room.locked_exits[direction]
        self.ui.display_text(f"The path to {next_room.name} is locked ({lock_id})")
        time.sleep(1)

        key_item = self.find_key(lock_id)

        # if the key is not in the player's storage then don't ask if they want to unlock
        if not key_item:
            return True

        self.display_key_options(key_item, next_room, room)

        return True

    def display_key_options(self, key_item, next_room, current_room):
        """
        Displays the options that shows up when the player attempts to go through a locked exit with a desired key
        in the player's storage.
        :param key_item: The key to unlock the exit.
        :param next_room: The room that the player will go inside.
        :param current_room: The room that the player is currently in.
        :return: None
        """
        # prompt to use key
        self.ui.clear_logs()
        self.ui.display_text(f"Use {key_item.name} to unlock?")
        self.ui.display_text("\n[1] Yes\n[2] No")

        key = self.game.menu.wait_for_key()
        if key == "ESC":
            self.game.menu.pause()

        # check for valid item selection
        if key == "1":
            self.ui.clear_logs()
            # check if the player is in the obsolete hub and if the decrypter has been used before unlocking
            if current_room.name == "obsolete_hub" and not current_room.kernel_unlock:
                self.ui.display_text("You need to activate the decrypter.")
            else:
                self.game.do_use(key_item)
                time.sleep(1)
                self.game.player.current_room = next_room
                self.ui.draw_room(self.game.player.current_room.describe())
        elif key == "2":
            self.ui.clear_logs()

    def find_key(self, lock_id):
        """
        Find a key item matching the lock ID in player's inventory.
        :param lock_id: The lock id of the room.
        :return: The key item if there is, None otherwise.
        """
        for item in self.game.player.storage.values():
            if isinstance(item, Key) and item.key_id == lock_id:
                return item
        return None
