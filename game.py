import curses
import time

from entities.characters.player import Player
from systems.inventory import Inventory
from systems.text_ui import TextUI
from world.world_builder import WorldBuilder
from entities.items.key import Key
from systems.combat import Combat
from systems.menu import Menu
from systems.input_handler import InputHandler
from systems.solver import Solver


class Game:
    """
    Main game controller managing game state, player commands, and interactions
    between player, world, and UI components.
    """
    # Game constants
    ESCAPE_CHANCE = 0.6
    INTRO_DELAY = 5
    ROOM_DELAY = 2

    def __init__(self):
        """Initialize game components."""
        self.movement_map = {
            curses.KEY_UP: "north",
            curses.KEY_DOWN: "south",
            curses.KEY_LEFT: "west",
            curses.KEY_RIGHT: "east"
        }
        self.player = Player("Lapel", "", 500, 500, 50)
        self.ui = TextUI()
        self.world = WorldBuilder()
        self.game_over = False
        self.menu = Menu(self.ui, self)
        self.input_handler = InputHandler(self)
        self.inventory = Inventory(self.ui, self)
        self.solver = Solver(self.ui, self.player, self)
        self.pause = False

    def run(self):
        """Entry point for the game. Handles UI lifecycle safely."""
        self.ui.start()
        try:
            result = self.play()
            if result:
                return result

            if self.game_over and not self.player.is_alive():
                return self.menu.game_over()
            return "quit"
        finally:
            self.ui.stop()

    def play(self):
        """Main game loop."""
        self._initialize_game()

        while not self.game_over:
            # Check for pause BEFORE getting new input
            if self.pause:
                # Trigger the pause menu
                action = self.menu.pause()

                # Handle the menu's return value
                if action == "restart":
                    return "restart"  # Exit play immediately to restart
                elif action == "quit":
                    return "quit"  # Exit play immediately to quit
                # If action is None, we simply loop again (Resume)

            self.ui.draw_hud(self.player)
            key = self.ui.get_key()
            self.input_handler.handle(key)
        return None

    def _initialize_game(self):
        """Set up the game world and display intro."""
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.print("""
> INITIALISING SESSION...
> LOADING USER MEMORY.............
> CHECKSUM ERROR IN SECTOR 0

[ WARNING ]
Your consciousness has been loaded into an unstable system.

Fragments of memory are missing.
Paths are corrupted.
Something hostile is running in the background.

You don't remember how you got here.
You don't remember who you were.

You only know one thing:
YOU MUST REACH THE KERNEL
AND ESCAPE BEFORE THE SYSTEM COLLAPSES
                      """)

        self.ui.wait_for_key()
        self.ui.draw_room(self.player.current_room.describe())
        self.ui.draw_hud(self.player)
        self.ui.clear_logs()
        self.ui.print("Press '/' for available commands.")
        self.ui.print("Hint: use arrow keys to move and [R] to scan room.")

    def wait_for_valid_key(self):
        while True:
            key = self.ui.get_key()
            if key != -1:
                return key

    def restart_game(self):
        """Reset game state for a new playthrough."""
        self.player = Player("Lapel", "", 500, 500, 50)
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.clear()
        self.ui.redraw_game(self.player.current_room, self.player)
        self.ui.print("Press '/' for available commands.")

    # __movement__

    def move(self, direction):
        """Move player in the specified direction."""
        room = self.player.current_room
        self.ui.print(f"Moving {direction}...")
        time.sleep(0.3)

        if direction not in room.exits:
            self.ui.print("You can't go that way!", False)
            return

        next_room = room.get_exit(direction)

        # Check for blocking monsters
        if self.check_monster_block(direction):
            return

        # Check for locked exits
        if self.check_locked_exit(direction, next_room):
            return

        # Move to next room
        self.player.current_room = next_room
        self.ui.clear()
        self.ui.draw_room(self.player.current_room.describe())

    def check_monster_block(self, direction):
        """Check if a monster is blocking the exit."""
        room = self.player.current_room
        for monster in room.monsters.values():
            if monster.blocks_exit == direction:
                self.ui.clear_logs()
                self.ui.print(f"{monster.name} has blocked you!")
                self.ui.print("Defeating it is the only way in...")
                time.sleep(1)
                self.ui.print("")
                self.do_fight(monster.name)
                return True
        return False

    def check_locked_exit(self, direction, next_room):
        """Check if exit is locked and handle unlocking."""
        room = self.player.current_room

        if direction not in room.locked_exits:
            return False

        lock_id = room.locked_exits[direction]
        self.ui.print(f"The path to {next_room.name} is locked ({lock_id})")
        time.sleep(1)

        # Find key in player's inventory
        key_item = self.find_key(lock_id)

        if not key_item:
            return True

        # Prompt to use key
        self.ui.clear_logs()
        self.ui.print(f"Use {key_item.name} to unlock?")
        self.ui.print("\n[1] Yes\n[2] No")

        key = self.wait_for_valid_key()
        if key == "ESC":
            self.menu.pause()

        # Check for valid item selection
        if key == "1":
            self.ui.clear_logs()
            if room.name == "obsolete_hub" and not room.kernel_unlock:
                self.ui.print("You need to activate the decrypter.")
            else:
                self.do_use(key_item)
                time.sleep(1)
                self.player.current_room = next_room
                self.ui.draw_room(self.player.current_room.describe())
        elif key == "2":
            self.ui.clear_logs()
        return True

    def find_key(self, lock_id):
        """Find a key item matching the lock ID in player's inventory."""
        for item in self.player.storage.values():
            if isinstance(item, Key) and item.key_id == lock_id:
                return item
        return None

    # ___room interaction___

    def scan_room(self):
        """Scan and display all entities in the current room."""
        room = self.player.current_room

        if not room.items and not room.monsters and not room.puzzle:
            self.ui.print("The room reveals nothing unusual.")
            return

        self.ui.print("Scanning", end="")
        for i in range(3):
            time.sleep(0.5)
            self.ui.print(".", end="")

        self.ui.print("\n", False)
        time.sleep(0.5)

        # Display items
        if room.items:
            self.ui.print("[ Items Detected ]", False)
            for item_name in room.items:
                self.ui.print(f" - {item_name}")
            self.ui.print("")
        else:
            self.ui.print("\n[ No Items Detected ]\n", False)
            self.ui.print("")

        # Display monsters
        if room.monsters:
            self.ui.print("[ Hostile Entities ]", False)
            for monster in room.monsters.values():
                self.ui.print(f" - {monster.name}")
            self.ui.print("")
        else:
            self.ui.print("[ No Hostiles Present ]\n", False)
            self.ui.print("")

        # Display puzzle
        if room.puzzle:
            self.ui.print("[ Corrupted Engram Detected ]", False)
            self.ui.print(f" {room.puzzle.name}\n")
            self.ui.print("")

        # Check for phantom key
        if "phantom_key" in self.player.storage:
            self.ui.print("[ Spatial Anomaly Detected ]", False)
            self.ui.print("A faint doorway signature is flickering here...\n")
            self.ui.print("")

    def take_item(self):
        """Pick up an item from the current room."""
        room = self.player.current_room

        if not room.items:
            self.ui.print("There are no items to pick up.")
            return

        selections = self.display_item_menu(room.items, "Pick an item:")

        key = self.wait_for_valid_key()
        if key == "ESC":
            self.menu.pause()

        # Check for valid item selection
        if key in selections:
            self.ui.clear_logs()
            chosen_item = selections[key]
            msg, _ = self.player.pick_up(chosen_item, self.ui)
            self.ui.print(msg)
            return  # Exit menu after inspecting

        # Check for Exit command
        if key == "b":
            self.ui.clear_logs()
            return

    def display_item_menu(self, items, prompt):
        """Display numbered menu of items and return selection mapping."""
        selections = {}
        self.ui.print(prompt)

        for i, (item_name, item) in enumerate(items.items(), start=1):
            self.ui.print(f"[{i}] {item_name}")
            selections[str(i)] = item
        self.ui.print("[B] Back")

        return selections

    def heal_player(self):
        """Use equipped medical item to heal player."""
        if not self.player.equipped_med:
            self.ui.print("You don't have any meds equipped!")
            return False

        med = self.player.equipped_med

        if self.player.hp == self.player.max_hp:
            self.ui.print("You are at max hp!")
            return False

        msg, flag = med.use(self.player)
        self.ui.print(f"You use {med.name}. {msg}")

        if flag == "remove":
            self.ui.print("Med charges depleted!")
            self.ui.print(self.player.remove_item(med))
        return True

    # __combat__

    def do_fight(self, monster_name):
        """Handle combat with a monster."""
        room = self.player.current_room

        if not room.monsters:
            self.ui.print("There is nothing here to fight.")
            return

        if monster_name not in room.monsters:
            self.ui.print("Invalid name.")
            return

        monster = room.monsters[monster_name]
        battle = Combat(self.ui, self.player, monster, self)
        battle.start()

        self.handle_combat_end(monster, self.player.current_room)

    def handle_combat_end(self, monster, room):
        """Handle post-combat rewards and consequences."""
        time.sleep(2)
        self.ui.clear_logs()

        if monster.hp == 0:
            self.ui.print(f"{monster.name} has fallen.")
            self.handle_monster_reward(monster, room)
            room.remove_monster(monster)

        if self.player.hp == 0:
            self.ui.clear_logs()
            self.ui.print("The pixels start to fade...")
            time.sleep(1)
            self.ui.print("OBJECTIVE FAILED")
            self.game_over = True
            time.sleep(3)

    def handle_monster_reward(self, monster, room):
        """Handle monster reward drops."""
        if not monster.reward:
            return

        self.ui.print(f"You have received: {monster.reward.name}\n")
        msg, picked_up = self.player.pick_up(monster.reward, self.ui)
        self.ui.print(msg)

        if not picked_up:
            room.add_item(monster.reward)
            self.ui.print(f"{monster.reward.name} has fallen to the floor.")

    def do_use(self, item):
        """Use an item from player's inventory."""

        result, flag = item.use(player=self.player, room=self.player.current_room)

        if result:
            self.ui.print(result)
            if flag == "remove":
                self.ui.print(self.player.remove_item(item))
        else:
            self.ui.print(f"You can't use {item.name} here.")

    def do_drop(self, item):
        """Drop an item from inventory into the current room."""
        room = self.player.current_room

        if item.name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        self.ui.print(self.player.remove_item(item))
        room.add_item(item)
        self.ui.print(f"{item.name} has fallen to the floor.")

    # ==================== HELP SYSTEM ====================

    def print_help(self):
        """Display all available commands."""
        self.ui.print("""COMMANDS:
Player:
  [ARROW KEYS]       - Move to another room
  [I]                - View player's statistics
  [S]                - View player's storage
  [H]                - Heal player if healing item equipped

Item Interaction:
  [T]                - Pick up an item in the room
  [R]                - Scan all entities in the room

Puzzles:
  [P]                - Attempt to solve the room's puzzle

System:
  [/]                - Show this help message
  [ESC]              - Pause menu
        """, False)


def main():
    """Main entry point for the game."""
    while True:
        game = Game()
        result = game.run()

        if result == "quit":
            break


if __name__ == "__main__":
    main()