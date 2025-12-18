import time
import logging
import sys
import os

# adds the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_code.entities.characters.player import Player
from game_code.entities.items.med import Med
from game_code.entities.items.weapon import Weapon
from game_code.systems.storage_handler import StorageHandler
from game_code.systems.text_ui import TextUI
from game_code.world.world_builder import WorldBuilder
from game_code.systems.combat import Combat
from game_code.systems.menu import Menu
from game_code.systems.input_handler import InputHandler
from game_code.systems.puzzle_handler import PuzzleHandler
from game_code.systems.movement import Movement

logging.basicConfig(filename="game.log", level=logging.INFO)


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
        self.player = Player("Lapel", "", 500, 500, 50)
        self.ui = TextUI()
        self.world = WorldBuilder()
        self.game_over = False
        self.menu = Menu(self.ui, self)
        self.input_handler = InputHandler(self)
        self.storage_handler = StorageHandler(self.ui, self)
        self.puzzle_handler = PuzzleHandler(self.ui, self.player)
        self.pause = False
        self.movement = Movement(self.ui, self)

    def run(self):
        """
        Entry point for the game and handles the UI lifecycle safely.
        :return: The game over menu if the player dies, or a result in which the player can quit or restart the game.
        """
        self.ui.start_screen()
        try:
            result = self.play()
            if result:
                return result

            if self.game_over and not self.player.is_alive():
                logging.info("Player dies")
                return self.menu.game_over_menu()  # return the menu for when the player dies
            return "quit"
        finally:
            self.ui.stop_screen()

    def play(self):
        """
        Main game loop that plays the game and constantly checks if the user has paused the game.
        :return: None
        """
        self.initialise_game()

        while not self.game_over:
            # check for pause
            if self.pause:
                # get pause menu
                action = self.menu.pause_menu()
                logging.info("User pauses the game")

                # handle menu's return value
                if action == "restart":
                    logging.info("User restarts the game")
                    return "restart"  # exit the play method to immediately restart the game
                elif action == "quit":
                    logging.info("User quits the game")
                    return "quit"  # exit the play method to quit the game
                # if there's no action, the game is resumed

            self.ui.draw_hud(self.player)
            key = self.ui.get_key()
            self.input_handler.handle(key)
            time.sleep(0.01) # reduces cpu load
        return None

    def initialise_game(self):
        """
        Set up the game world and display intro.
        :return: None
        """
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.print_welcome()
        self.ui.wait_to_start_game()
        self.ui.draw_room(self.player.current_room.describe())
        self.ui.draw_hud(self.player)
        self.ui.clear_logs()
        self.ui.display_text("Press '/' for available commands.")
        self.ui.display_text("Hint: use arrow keys to move and [R] to scan room.")

    def move(self, direction):
        """
        Move player in the specified direction.
        :return: None
        """
        if self.movement.try_move(self.player, direction):
            logging.info(f"Player moved {direction} to {self.player.current_room.name}")
            self.ui.clear()
            self.ui.draw_room(self.player.current_room.describe())

    def scan_room(self):
        """
        Scan and display all entities in the current room.
        :return: None
        """
        room = self.player.current_room

        self.ui.display_text("Scanning", end="")
        for i in range(3):
            time.sleep(0.5)
            self.ui.display_text(".", end="")
        self.ui.display_text("\n", False)
        time.sleep(0.5)

        if not room.items and not room.monsters and not room.puzzle:
            self.ui.clear_logs()
            self.ui.display_text("The room reveals nothing unusual.")
            time.sleep(1)
            self.ui.clear_logs()
            return

        # display items
        if room.items:
            self.ui.display_text("[ Items Detected ]", False)
            for item_name in room.items:
                self.ui.display_text(f" - {item_name}")
            self.ui.display_text("")
        else:
            self.ui.display_text("\n[ No Items Detected ]\n", False)
            self.ui.display_text("")

        # display monsters
        if room.monsters:
            self.ui.display_text("[ Hostile Entities ]", False)
            for monster in room.monsters.values():
                self.ui.display_text(f" - {monster.name}")
            self.ui.display_text("")
        else:
            self.ui.display_text("[ No Hostiles Present ]\n", False)
            self.ui.display_text("")

        # display puzzle
        if room.puzzle:
            self.ui.display_text("[ Corrupted Engram Detected ]", False)
            self.ui.display_text(f" {room.puzzle.name}\n")
            self.ui.display_text("")

        # check for phantom key
        if "phantom_key" in self.player.storage:
            self.ui.display_text("[ Spatial Anomaly Detected ]", False)
            self.ui.display_text("A faint doorway signature is flickering here...\n")
            self.ui.display_text("")

    def display_items(self):
        """
        Display items for the player to take in the room.
        :return: None
        """
        room = self.player.current_room

        if not room.items:
            self.ui.display_text("There are no items to pick up.")
            return

        selections = self.menu.item_menu(room.items, "Pick an item:")

        key = self.ui.wait_for_key()
        self.choose_item(key, selections)

    def choose_item(self, key, selections):
        """
        Pick the item that the player chooses using a key.
        :param key: The key that the user presses.
        :param selections: The items that can be selected.
        :return: None
        """
        if key == "ESC":
            self.menu.pause_menu()

        # check for valid item selection
        if key in selections:
            self.ui.clear_logs()
            chosen_item = selections[key]
            picked_up = self.player.pick_up(chosen_item)
            prev_weight = self.player.weight
            if not picked_up:
                self.ui.display_text(f"{chosen_item.name} is too heavy to carry.")
            elif picked_up:
                self.ui.display_text(f"{chosen_item.name} added to storage.")
                self.ui.display_text(f"Storage: {prev_weight} + {chosen_item.weight} --> "
                                     f"{self.player.weight}/{self.player.max_weight} bytes")
                time.sleep(1)
                self.ui.clear_logs()
                logging.info(f"Player picked up {chosen_item.name}")

                prompt_msg = None
                if isinstance(chosen_item, Weapon) and chosen_item.damage > self.player.attack_power:
                    prompt_msg = f"{chosen_item.name} is stronger than your current attack power. Equip?"

                elif isinstance(chosen_item, Med) and self.player.equipped_med is None:
                    prompt_msg = "You don't have any meds currently equipped. Equip?"

                if prompt_msg:
                    self.ui.display_text(prompt_msg)
                    self.ui.display_text("[1] Yes\n[2] No")

                    while True:
                        key = self.ui.wait_for_key()
                        if key == -1: continue

                        if key == "1":
                            msg = self.player.equip(chosen_item)
                            self.ui.clear_logs()
                            self.ui.display_text(msg)
                            logging.info(f"Player equipped {chosen_item.name}")
                            break
                        elif key == "2":
                            self.ui.clear_logs()
                            break

            return  # exit menu after inspecting

        # check for exit command
        if key == "b":
            self.ui.clear_logs()
            return

    def heal_player(self):
        """
        Use equipped medical item to heal player.
        :return: True if the player was healed, False otherwise.
        """
        if not self.player.equipped_med:
            self.ui.display_text("You don't have any meds equipped!")
            return False

        med = self.player.equipped_med

        if self.player.hp == self.player.max_hp:
            self.ui.display_text("You are at max hp!")
            return False

        msg, flag = med.use(self.player)
        self.ui.display_text(f"You use {med.name}. {msg}")
        logging.info("Player heals")

        if flag == "remove":
            self.ui.display_text("Med charges depleted!")
            self.ui.display_text(self.player.remove_item(med))
        return True

    def do_fight(self, monster_name):
        """
        Handle combat with a monster.
        :param monster_name: The name of the monster in which teh player is fighting.
        :return: None
        """
        room = self.player.current_room

        if not room.monsters:
            self.ui.display_text("There is nothing here to fight.")
            return

        if monster_name not in room.monsters:
            self.ui.display_text("Invalid name.")
            return

        monster = room.monsters[monster_name]
        battle = Combat(self.ui, self.player, monster, self)
        logging.info("Player starts fight")
        battle.start()

    def do_use(self, item):
        """
        Use an item from player's storage, where it is removed if it can be used.
        :param item: The item that is being used.
        """

        result, flag = item.use(player=self.player)

        if result:
            self.ui.display_text(result)
            if flag == "remove":
                self.ui.display_text(self.player.remove_item(item))
                logging.info(f"Player uses {item.name}")
        else:
            self.ui.display_text(f"You can't use {item.name} here.")

    def do_drop(self, item):
        """
        Drop an item from storage into the current room.
        :param item: The item is dropped.
        """
        if item.name not in self.player.storage:
            self.ui.display_text("You don't have that item.")
            return

        self.ui.display_text(self.player.remove_item(item))
        self.ui.display_text(f"{item.name} has fallen to the floor.")
        logging.info(f"Player drops {item.name}")


def main():
    """
    Main entry point for the game.
    """
    while True:
        logging.info("User starts a new game")
        game = Game()
        result = game.run()

        if result == "quit":
            break

if __name__ == "__main__":
    main()
