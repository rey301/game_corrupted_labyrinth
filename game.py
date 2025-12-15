import curses
import time
from random import random

from player import Player
from text_ui import TextUI
from world_builder import WorldBuilder
from weapon import Weapon
from consumable import Consumable
from misc import Misc


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
        self.player = Player("Lapel", "", 500, 500, 50)
        self.ui = TextUI()
        self.world = WorldBuilder()
        self.game_over = False

    def run(self):
        """Entry point for the game. Handles UI lifecycle safely."""
        self.ui.start()
        try:
            self.play()
            if self.game_over and not self.player.is_alive():
                return self.game_over_menu()
            return "quit"
        finally:
            self.ui.stop()

    def play(self):
        """Main game loop."""
        self._initialize_game()

        while not self.game_over and self.player.is_alive():
            key = self.ui.get_key()
            self.handle_key(key)

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

    # ==================== MENU SYSTEMS ====================

    def game_over_menu(self):
        """Display game over menu and handle selection."""
        text = (
            "=== SYSTEM FAILURE ===\n"
            "You have been terminated.\n\n"
            "[R] Restart\n"
            "[Q] Quit"
        )
        self.ui.draw_top(text)

        while True:
            key = self.ui.get_key()
            if key == "r":
                self.ui.clear()
                return "restart"
            elif key == "q":
                return "quit"

    def pause_menu(self):
        """Display pause menu and handle selection."""
        self.ui.draw_top(
            "=== SYSTEM PAUSED ===\n\n"
            "[ESC] Resume\n"
            "[R] Restart\n"
            "[Q] Quit"
        )

        while True:
            key = self.ui.get_key()

            if key == "ESC":
                self.ui.redraw_game(self.player.current_room, self.player)
                return
            elif key == "r":
                self._restart_game()
                return
            elif key == "q":
                self.game_over = True
                return

    def _restart_game(self):
        """Reset game state for a new playthrough."""
        self.player = Player("Lapel", "", 500, 500, 50)
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.clear()
        self.ui.redraw_game(self.player.current_room, self.player)
        self.ui.print("Press '/' for available commands.")

    # ==================== INPUT HANDLING ====================

    def handle_key(self, key):
        """Process player key input and execute corresponding action."""
        if key == -1:
            return

        self.ui.clear_logs()
        # Movement keys
        movement_map = {
            curses.KEY_UP: "north",
            curses.KEY_DOWN: "south",
            curses.KEY_LEFT: "west",
            curses.KEY_RIGHT: "east"
        }

        if key in movement_map:
            self.ui.print(f"Moving {movement_map[key]}...")
            time.sleep(0.5)
            self.move(movement_map[key])
            self.ui.draw_hud(self.player)

            return
        # Action keys
        elif key == "r":
            self.scan_room()
        elif key == "p":
            self.do_solve()
        elif key == "t":
            self.take_item()
        elif key == "h":
            self.heal_player()
        elif key == "s":
            self.show_player_storage()
        elif key == "i":
            self.ui.print(self.player.show_stats())
        elif key == "/":
            self.print_help()
        elif key == "ESC":
            self.pause_menu()
            return
        elif key != " ":
            self.ui.print("Unknown command.")
            self.ui.print("Press '/' for available commands.")

        self.ui.draw_hud(self.player)

    # ==================== MOVEMENT ====================

    def move(self, direction):
        """Move player in the specified direction."""
        room = self.player.current_room

        if direction not in room.exits:
            self.ui.print("You can't go that way!")
            return

        next_room = room.get_exit(direction)

        # Check for blocking monsters
        if self._check_monster_block(direction):
            return

        # Check for locked exits
        if self._check_locked_exit(direction, next_room):
            return

        # Move to next room
        self.player.current_room = next_room
        self.ui.clear()
        self.ui.draw_room(self.player.current_room.describe())

    def _check_monster_block(self, direction):
        """Check if a monster is blocking the exit."""
        room = self.player.current_room
        for monster in room.monsters.values():
            if monster.blocks_exit == direction:
                self.ui.clear_logs()
                self.ui.print(f"{monster.name} has blocked you!")
                self.ui.print("Defeating it is the only way in...")
                self.do_fight(monster.name)
                return True
        return False

    def _check_locked_exit(self, direction, next_room):
        """Check if exit is locked and handle unlocking."""
        room = self.player.current_room

        if direction not in room.locked_exits:
            return False

        lock_id = room.locked_exits[direction]
        self.ui.print(f"The path to {next_room.name} is locked ({lock_id})")
        time.sleep(1)

        # Find key in player's inventory
        key_item = self._find_key_for_lock(lock_id)

        if not key_item:
            return True

        # Prompt to use key
        self.ui.clear_logs()
        self.ui.print(f"Use {key_item.name} to unlock?")
        self.ui.print("\n[1] Yes\n[2] No")

        while True:
            key = self.ui.get_key()

            # If no key is pressed (and we are in non-blocking mode),
            # get_key returns -1. We must ignore it and keep waiting.
            if key == -1:
                continue

            # Check for valid item selection
            if key == "1":
                if room.name == "obsolete_hub" and not room.kernel_unlock:
                    self.ui.print("You need to activate the decrypter.")
                else:
                    self.ui.clear_logs()
                    self.do_use(key_item)
                    time.sleep(1)
                    self.player.current_room = next_room
                    self.ui.draw_room(self.player.current_room.describe())
                break
            elif key == "2":
                self.ui.clear_logs()
                break

        return True

    def _find_key_for_lock(self, lock_id):
        """Find a key item matching the lock ID in player's inventory."""
        for item in self.player.storage.values():
            if isinstance(item, Misc) and item.misc_id == lock_id:
                return item
        return None

    # ==================== ROOM INTERACTION ====================

    def scan_room(self):
        """Scan and display all entities in the current room."""
        room = self.player.current_room

        if not room.items and not room.monsters and not room.puzzle:
            self.ui.print("The room reveals nothing unusual.")
            return

        lines = ["Scanning...\n"]

        # Display items
        if room.items:
            lines.append("[ Items Detected ]")
            for item_name in room.items:
                lines.append(f" - {item_name}")
            lines.append("")
        else:
            lines.append("[ No Items Detected ]\n")

        # Display monsters
        if room.monsters:
            lines.append("[ Hostile Entities ]")
            for monster in room.monsters.values():
                lines.append(f" - {monster.name}")
            lines.append("")
        else:
            lines.append("[ No Hostiles Present ]\n")

        # Display puzzle
        if room.puzzle:
            lines.append("[ Corrupted Engram Detected ]")
            lines.append(f" - {room.puzzle.name}\n")

        # Check for phantom key
        if "phantom_key" in self.player.storage:
            lines.append("[ Spatial Anomaly Detected ]")
            lines.append("A faint doorway signature is flickering here...\n")

        self.ui.print("\n".join(lines))

    def take_item(self):
        """Pick up an item from the current room."""
        room = self.player.current_room

        if not room.items:
            self.ui.print("There are no items to pick up.")
            return

        selections = self._display_item_menu(room.items, "Pick an item:")

        while True:
            key = self.ui.get_key()

            # If no key is pressed (and we are in non-blocking mode),
            # get_key returns -1. We must ignore it and keep waiting.
            if key == -1:
                continue

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

    def _display_item_menu(self, items, prompt):
        """Display numbered menu of items and return selection mapping."""
        selections = {}
        self.ui.print(prompt)

        for i, (item_name, item) in enumerate(items.items(), start=1):
            self.ui.print(f"[{i}] {item_name}")
            selections[str(i)] = item

        return selections

    # ==================== COMBAT ====================

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
        self._display_combat_start(monster)

        # Combat loop
        while self.player.is_alive() and monster.is_alive():
            action = self._get_combat_action()

            if action == "retreat":
                if self._attempt_retreat(monster):
                    return
                continue
            elif action == "heal":
                self.heal_player()
            elif action == "attack":
                self._execute_attack(monster)
            else:
                self.ui.print("Invalid action.")
                continue

            if not monster.is_alive():
                break

            # Monster's turn
            self._monster_attack(monster)

        # Handle combat end
        self._handle_combat_end(monster, room)

    def _display_combat_start(self, monster):
        """Display combat initiation messages."""
        self.ui.print(f"You engage the {monster.name}")
        self.ui.print(f"{monster.name} HP: {monster.hp}/{monster.max_hp}")
        self.ui.print(f"Your HP: {self.player.hp}/{self.player.max_hp}")

    def _get_combat_action(self):
        """Display combat menu and get player's action."""
        self.ui.print("\nChoose your action:")
        self.ui.print("[1] Attack")
        self.ui.print("[2] Heal")
        self.ui.print("[3] Retreat")

        msg = None

        while True:

            action = self.ui.get_key()

            if action == -1:
                continue
            action_map = {"1": "attack", "2": "heal", "3": "retreat"}
            msg = action_map.get(action, "invalid")
            self.ui.clear_logs()
            break

        return msg

    def _execute_attack(self, monster):
        """Execute player attack on monster."""
        damage = self.player.attack(monster)
        monster_hp = monster.hp

        if self.player.equipped_weapon is None:
            self.ui.print("Warning! You have no weapon equipped.")
            self.ui.print(f"You strike the {monster.name} with your fists for {damage}")
            self.ui.print(f"{monster.name} HP: {monster_hp} - {damage} --> {monster.hp}/{monster.max_hp}")
        else:
            weapon_name = self.player.equipped_weapon.name
            self.ui.print(f"You strike the {monster.name} with {weapon_name} for {damage}")
            self.ui.print(f"{monster.name} HP: {monster_hp} - {damage} --> {monster.hp}/{monster.max_hp}")

        return damage

    def _monster_attack(self, monster):
        """Execute monster attack on player."""
        player_hp = self.player.hp
        damage = monster.attack(self.player)

        self.ui.print(f"The {monster.name} hits you for {damage} damage.")
        self.ui.print(f"Player HP: {player_hp} - {damage} --> {self.player.hp}/{self.player.max_hp}")
        self.ui.draw_hud(self.player)

    def _attempt_retreat(self, monster):
        """Attempt to retreat from combat."""
        if random() < self.ESCAPE_CHANCE:
            self.ui.print("You successfully retreat from the fight!")
            return True

        self.ui.print("Retreat failed! The monster strikes as you turn away!")
        damage = monster.attack(self.player)
        self.ui.print(f"The {monster.name} hits you for {damage} damage.")
        self.ui.print(f"Your HP: {self.player.hp}/{self.player.max_hp}")

        if not self.player.is_alive():
            self.ui.print("You collapse while trying to escape...")
            self.game_over = True
            return True

        return False

    def _handle_combat_end(self, monster, room):
        """Handle post-combat rewards and consequences."""
        if monster.hp == 0:
            self.ui.print(f"{monster.name} has fallen.")
            self._handle_monster_reward(monster, room)
            room.remove_monster(monster)

        if self.player.hp == 0:
            self.ui.print("You have been defeated...")
            self.game_over = True

    def _handle_monster_reward(self, monster, room):
        """Handle monster reward drops."""
        if not monster.reward:
            return

        self.ui.print(f"You have received: {monster.reward.name}\n")
        msg, picked_up = self.player.pick_up(monster.reward, self.ui)
        self.ui.print(msg)

        if not picked_up:
            room.add_item(monster.reward)
            self.ui.print(f"{monster.reward.name} has fallen to the floor.")

    # ==================== ITEM MANAGEMENT ====================

    def heal_player(self):
        """Use equipped medical item to heal player."""
        if not self.player.equipped_med:
            self.ui.print("You don't have any meds equipped!")
            return

        med = self.player.equipped_med

        if self.player.hp == self.player.max_hp:
            self.ui.print("You are at max hp!")
            return

        msg, flag = med.use(self.player)
        self.ui.print(f"You use {med.name}. {msg}")

        if flag == "remove":
            self.ui.print("Med charges depleted!")
            self.ui.print(self.player.remove_item(med))

    def do_use(self, item):
        """Use an item from player's inventory."""
        if item.name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        # Weapons can't be used, only equipped
        if isinstance(item, Weapon):
            self.ui.print(f"You can't 'use' {item.name}. Try equipping it instead.")
            return

        # Consumables heal the player
        if isinstance(item, Consumable):
            if self.player.hp == self.player.max_hp:
                self.ui.print("You are at max hp!")
            else:
                healed, _ = item.use(self.player)
                self.ui.print(f"You use {item.name}. {healed}")
                self.ui.print(self.player.remove_item(item.name))
            return

        # Misc items have special uses
        if isinstance(item, Misc):
            result, flag = item.use(self.player, self.player.current_room, self.world)

            if result:
                self.ui.print(result)
                if flag == "remove":
                    self.ui.print(self.player.remove_item(item))
            else:
                self.ui.print(f"You can't use {item.name} here.")
            return

        self.ui.print("Nothing happens.")

    def do_drop(self, item):
        """Drop an item from inventory into the current room."""
        room = self.player.current_room

        if item.name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        self.ui.print(self.player.remove_item(item))
        room.add_item(item)
        self.ui.print(f"{item.name} has fallen to the floor.")

    # ==================== INVENTORY SYSTEM ====================

    def show_player_storage(self):
        """Display player's inventory with item selection."""
        storage = self.player.storage

        if not storage:
            self.ui.print("Your storage is empty.")
            return

        selections = {}
        self.ui.print("[ STORAGE ]\n")

        for i, (name, item) in enumerate(storage.items(), start=1):
            self.ui.print(f"[{i}] {name} (W:{item.weight})")
            selections[str(i)] = item

        self.ui.print("[B] Go back")
        self.ui.print(f"\n[ CAP <{self.player.weight}/{self.player.max_weight}> ]")

        # 2. THE FIX: Loop specifically for this menu
        while True:
            key = self.ui.get_key()

            # If no key is pressed (and we are in non-blocking mode),
            # get_key returns -1. We must ignore it and keep waiting.
            if key == -1:
                continue

            # Check for valid item selection
            if key in selections:
                self.inspect_item(selections[key])
                return  # Exit menu after inspecting

            # Check for Exit command
            if key == "b":
                self.ui.clear_logs()
                return

    def inspect_item(self, item):
        """Display item details and available actions."""
        self.ui.clear_logs()

        self.ui.print(f"[ {item.name} ]")
        self.ui.print(f"{item.description}\n")

        actions = self._get_item_actions(item)

        for key, label, _ in actions:
            self.ui.print(f"[{key}] {label}")
        self.ui.print("[B] Go back")

        while True:
            choice = self.ui.get_key()

            if choice == -1:
                continue

            for key, _, action in actions:
                if choice == key:
                    self.ui.clear_logs()
                    msg = action()
                    if msg:
                        self.ui.print(msg)
                    return
                # Check for Exit command
                if choice == "b":
                    self.ui.clear_logs()
                    self.show_player_storage()
                    return

    def _get_item_actions(self, item):
        """Get available actions for an item based on its type."""
        player = self.player
        actions = []

        if isinstance(item, Weapon):
            is_equipped = player.equipped_weapon == item
            actions.append((
                "1",
                "Unequip" if is_equipped else "Equip",
                lambda: self.ui.print(player.unequip(item) if is_equipped else player.equip(item))
            ))
            actions.append(("2", "Drop", lambda: self.do_drop(item)))

        elif isinstance(item, Consumable):
            is_equipped = player.equipped_med == item
            actions.append((
                "1",
                "Unequip" if is_equipped else "Equip",
                lambda: self.ui.print(player.unequip(item) if is_equipped else player.equip(item))
            ))
            actions.append(("2", "Use", lambda: self.heal_player()))
            actions.append(("3", "Drop", lambda: self.do_drop(item)))

        else:  # Misc items
            actions.append(("1", "Use", lambda: self.do_use(item)))
            actions.append(("2", "Drop", lambda: self.ui.print(player.remove_item(item))))

        return actions

    # ==================== PUZZLE SYSTEM ====================

    def do_solve(self):
        """Attempt to solve the puzzle in the current room."""
        room = self.player.current_room

        if room.puzzle is None:
            self.ui.print("There is no puzzle here.")
            return

        message, reward = room.puzzle.attempt(self.ui)
        self.ui.print(message)

        if room.puzzle.solved:
            room.remove_puzzle()

        if reward:
            self._handle_puzzle_reward(reward, room)

    def _handle_puzzle_reward(self, reward, room):
        """Handle reward from solving a puzzle."""
        self.ui.print(f"You have received: {reward.name}")
        msg, picked_up = self.player.pick_up(reward, ui=self.ui)
        self.ui.print(msg)

        if not picked_up:
            room.add_item(reward)
            self.ui.print(f"{reward.name} has fallen to the floor.")

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
  [R]                - List all entities in the room

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