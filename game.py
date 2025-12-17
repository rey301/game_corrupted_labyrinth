import curses
import time

from entities.characters.player import Player
from systems.inventory import Inventory
from systems.text_ui import TextUI
from world.world_builder import WorldBuilder
from systems.combat import Combat
from systems.menu import Menu
from systems.input_handler import InputHandler
from systems.solver import Solver
from systems.movement import Movement


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
        self.menu = Menu(self.ui, self)
        self.input_handler = InputHandler(self)
        self.inventory = Inventory(self.ui, self)
        self.solver = Solver(self.ui, self.player, self)
        self.pause = False
        self.movement = Movement(self.ui, self)

    def run(self):
        """Entry point for the game. Handles UI lifecycle safely."""
        self.ui.start()
        try:
            result = self.play()
            if result:
                return result

            if self.game_over and not self.player.is_alive():
                return self.menu.game_over_menu() # return the menu for when the player dies
            return "quit"
        finally:
            self.ui.stop()

    def play(self):
        """Main game loop."""
        self.initialise_game()

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

    def initialise_game(self):
        """Set up the game world and display intro."""
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.print_welcome()
        self.ui.wait_for_key()
        self.ui.draw_room(self.player.current_room.describe())
        self.ui.draw_hud(self.player)
        self.ui.clear_logs()
        self.ui.display_text("Press '/' for available commands.")
        self.ui.display_text("Hint: use arrow keys to move and [R] to scan room.")

    # movement

    def move(self, direction):
        """Move player in the specified direction."""
        # Move to next room
        if self.movement.try_move(self.player, direction):
            self.ui.clear()
            self.ui.draw_room(self.player.current_room.describe())

    # room interaction

    def scan_room(self):
        """Scan and display all entities in the current room."""
        room = self.player.current_room

        if not room.items and not room.monsters and not room.puzzle:
            self.ui.display_text("The room reveals nothing unusual.")
            return

        self.ui.display_text("Scanning", end="")
        for i in range(3):
            time.sleep(0.5)
            self.ui.display_text(".", end="")

        self.ui.display_text("\n", False)
        time.sleep(0.5)

        # Display items
        if room.items:
            self.ui.display_text("[ Items Detected ]", False)
            for item_name in room.items:
                self.ui.display_text(f" - {item_name}")
            self.ui.display_text("")
        else:
            self.ui.display_text("\n[ No Items Detected ]\n", False)
            self.ui.display_text("")

        # Display monsters
        if room.monsters:
            self.ui.display_text("[ Hostile Entities ]", False)
            for monster in room.monsters.values():
                self.ui.display_text(f" - {monster.name}")
            self.ui.display_text("")
        else:
            self.ui.display_text("[ No Hostiles Present ]\n", False)
            self.ui.display_text("")

        # Display puzzle
        if room.puzzle:
            self.ui.display_text("[ Corrupted Engram Detected ]", False)
            self.ui.display_text(f" {room.puzzle.name}\n")
            self.ui.display_text("")

        # Check for phantom key
        if "phantom_key" in self.player.storage:
            self.ui.display_text("[ Spatial Anomaly Detected ]", False)
            self.ui.display_text("A faint doorway signature is flickering here...\n")
            self.ui.display_text("")

    def take_item(self):
        """Pick up an item from the current room."""
        room = self.player.current_room

        if not room.items:
            self.ui.display_text("There are no items to pick up.")
            return

        selections = self.menu.display_item_menu(room.items, "Pick an item:")

        key = self.menu.wait_for_key()
        if key == "ESC":
            self.menu.pause()

        # Check for valid item selection
        if key in selections:
            self.ui.clear_logs()
            chosen_item = selections[key]
            msg, _ = self.player.pick_up(chosen_item, self.ui)
            self.ui.display_text(msg)
            return  # Exit menu after inspecting

        # Check for Exit command
        if key == "b":
            self.ui.clear_logs()
            return

    def heal_player(self):
        """Use equipped medical item to heal player."""
        if not self.player.equipped_med:
            self.ui.display_text("You don't have any meds equipped!")
            return False

        med = self.player.equipped_med

        if self.player.hp == self.player.max_hp:
            self.ui.display_text("You are at max hp!")
            return False

        msg, flag = med.use(self.player)
        self.ui.display_text(f"You use {med.name}. {msg}")

        if flag == "remove":
            self.ui.display_text("Med charges depleted!")
            self.ui.display_text(self.player.remove_item(med))
        return True

    # __combat__

    def do_fight(self, monster_name):
        """Handle combat with a monster."""
        room = self.player.current_room

        if not room.monsters:
            self.ui.display_text("There is nothing here to fight.")
            return

        if monster_name not in room.monsters:
            self.ui.display_text("Invalid name.")
            return

        monster = room.monsters[monster_name]
        battle = Combat(self.ui, self.player, monster, self)
        battle.start()

    # using items
    def do_use(self, item):
        """Use an item from player's inventory."""

        result, flag = item.use(player=self.player, room=self.player.current_room)

        if result:
            self.ui.display_text(result)
            if flag == "remove":
                self.ui.display_text(self.player.remove_item(item))
        else:
            self.ui.display_text(f"You can't use {item.name} here.")

    def do_drop(self, item):
        """Drop an item from inventory into the current room."""
        room = self.player.current_room

        if item.name not in self.player.storage:
            self.ui.display_text("You don't have that item.")
            return

        self.ui.display_text(self.player.remove_item(item))
        room.add_item(item)
        self.ui.display_text(f"{item.name} has fallen to the floor.")

def main():
    """Main entry point for the game."""
    while True:
        game = Game()
        result = game.run()

        if result == "quit":
            break


if __name__ == "__main__":
    main()