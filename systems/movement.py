import time
from entities.items.key import Key

class Movement:
    def __init__(self, ui, game):
        self.ui = ui
        self.game = game

    def try_move(self, player, direction):
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
        """Check if a monster is blocking the exit."""
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
        """Check if exit is locked and handle unlocking."""
        room = self.game.player.current_room

        if direction not in room.locked_exits:
            return False

        lock_id = room.locked_exits[direction]
        self.ui.display_text(f"The path to {next_room.name} is locked ({lock_id})")
        time.sleep(1)

        # Find key in player's inventory
        key_item = self.find_key(lock_id)

        if not key_item:
            return True

        # Prompt to use key
        self.ui.clear_logs()
        self.ui.display_text(f"Use {key_item.name} to unlock?")
        self.ui.display_text("\n[1] Yes\n[2] No")

        key = self.game.menu.wait_for_key()
        if key == "ESC":
            self.game.menu.pause()

        # Check for valid item selection
        if key == "1":
            self.ui.clear_logs()
            if room.name == "obsolete_hub" and not room.kernel_unlock:
                self.ui.display_text("You need to activate the decrypter.")
            else:
                self.game.do_use(key_item)
                time.sleep(1)
                self.game.player.current_room = next_room
                self.ui.draw_room(self.game.player.current_room.describe())
        elif key == "2":
            self.ui.clear_logs()
        return True

    def find_key(self, lock_id):
        """Find a key item matching the lock ID in player's inventory."""
        for item in self.game.player.storage.values():
            if isinstance(item, Key) and item.key_id == lock_id:
                return item
        return None