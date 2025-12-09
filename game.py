from player import Player
from parser import Parser
from world_builder import WorldBuilder
from text_ui import TextUI
from weapon import Weapon
from consumable import Consumable
from misc import Misc

class Game:
    """
        The main controller for the game, which manages the play() state,
        user commands, and coordinates interactions between the player,
        world, and UI. Parsing for commands is taken to the Parser,
        constructing the game world/map is done to the WorldBuilder,
        and user input/output to the TextUI.
    """

    def __init__(self):
        """
        Initialises the game.
        """

        self.player = Player("Lapel","",5, 5, 1)
        self.ui = TextUI()
        self.parser = Parser(self.ui)
        self.world = WorldBuilder()
        self.game_over = False

    def play(self):
        """
            The main play loop that displays welcome message, reads player input
            in a loop, processes commands, and terminates when game_over becomes
            True.
        :return: None
        """
        # initialise world and intro messages
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.print("Welcome to the Labyrinth. \nType HELP to see available commands.\n")
        self.ui.print(self.player.current_room.describe())

        # main game loop
        while not self.game_over and self.player.is_alive():
            command = self.parser.get_command()
            self.game_over = self.process(command)
        print("Thank you for playing!")


    def process(self, command):
        """
            Handles user commands and invokes an action method from
            the command given (e.g. item interaction, problem solving).
        :param command: Parse command object containing the verb and obj (optional)
        :return: True if game should end (quit or player dies), otherwise False if game continues
        """

        verb = command.verb
        obj = command.obj

        # unknown command
        if verb is None:
            self.ui.print("I don't understand that command.")
            return False

        # movement
        if verb == "go":
            self.do_go(obj)
            return False

        # looking for items in the room
        elif verb == "inspect":
            self.do_inspect(obj)
            return False

        # show inventory
        elif verb == "inventory":
            self.ui.print(self.player.show_inventory())
            return False

        # take item
        elif verb == "take":
            self.do_take(obj)
            return False

        # use item
        elif verb == "use":
            self.do_use(obj)
            return False

        # fight monster
        elif verb == "fight":
            self.do_fight()
            return False

        # solve puzzle
        elif verb == "solve":
            self.do_solve()
            return False

        # help menu
        elif verb == "help":
            self.print_help()
            return False

        # quit game
        elif verb == "quit":
            return True  # This ends the game loop

        # otherwise
        else:
            self.ui.print("That command is not implemented.")
            return False

    def do_go(self, direction):
        """
        Move player into room given the direction, and if exit doesn't exist;
        error message is displayed.
        :param direction: Direction the player wishes to move (e.g. north, east)
        """
        if direction is None:
            self.ui.print("Go where?")
            return
        next_room = self.player.current_room.get_exit(direction)

        if next_room is not None:
            self.player.current_room = next_room
            self.ui.print(self.player.current_room.describe())

    def do_inspect(self, obj):
        room = self.player.current_room
        if obj is None:
            self.ui.print("Inspect what?")
            return

        # inspecting an item in the room
        if obj in room.items:
            item = room.items[obj]
            self.ui.print(f"{item.name}: {item.description}")
            return

        if obj == "room":
            if not room.items:
                self.ui.print("There are no items to inspect here.")
                return

            self.ui.print("Items in this room:")

            for item_name, item in room.items.items():
                self.ui.print(f" - {item_name}: {item.description}")
            return

        # inspecting item in inventory
        if obj in self.player.inventory:
            item = self.player.inventory[obj]
            self.ui.print(f"{item.name}: {item.description}")
            return

        # inspecting a monster
        for monster in room.monsters:
            if monster.name.lower() == obj.lower():
                self.ui.print(f"{monster.name}: {monster.description}")
                return

        self.ui.print("You see nothing like that.")

    def do_take(self, item_name):
        """
        Attempt to pick up an item from the current room and put it in the
        player's backpack.
        :param item_name: Name of the item the player wishes to pick up.
        :return: None
        """
        room = self.player.current_room
        if item_name is None:
            self.ui.print("Take what?")
            return
        if item_name not in room.items:
            self.ui.print("That item is not here.")
            return

        item = room.items[item_name]
        prev_weight = self.player.weight
        success = self.player.pick_up(item)
        if success:
            self.ui.print(f"{item_name} added to backpack.")
            self.ui.print(f"Storage: {prev_weight} + {item.weight} --> {self.player.weight}/{self.player.max_weight} bytes")
            self.player.current_room.remove_item(item)
        else:
            self.ui.print(f"{item.name} is too heavy to carry.")

    def do_use(self, item_name):
        """
            Allows player to use an item from their backpack, applying whatever
            effect the item has.
        :param item_name: Name of the item to use.
        :return: None
        """
        if item_name is None:
            self.ui.print("Use what?")
            return

        if item_name not in self.player.inventory:
            self.ui.print("You don't have that item.")
            return

        item = self.player.inventory[item_name]

        # check if it's a weapon
        if isinstance(item, Weapon):
            self.ui.print(f"You can't 'use' {item.name}. Try 'equip {item.name}' instead.")
            return

        # for healing
        if isinstance(item, Consumable):
            healed = item.use(self.player)
            self.ui.print(f"You use {item.name}. {healed}")
            self.player.inventory.pop(item_name)
            return

        # for unlocking something
        if isinstance(item, Misc):
            result = item.use(self.player, self.player.current_room, self.world)

            if result:
                self.ui.print(result)
            else:
                self.ui.print(f"You can't use {item.name} here.")
            return

        self.ui.print("Nothing happens.")


    def do_fight(self):
        """
            Handles the combat with a monster in the current room, where combat
            alternates between player and the monster until one is defeated.
            Game is over if the player dies. If the monster dies, the player
            is rewarded and monster is removed from the room.
        :return: None
        """

    def do_solve(self):
        """
            Allows player to attempt to solve the puzzle in the current room.
        :return: None
        """
        self.puzzle.attempt()

    def print_help(self):
        """
        Prints a list of all available player commands.
        :return: None
        """
        self.ui.print("\nAvailable commands:\n")

        self.ui.print("Movement:")
        self.ui.print("  go <direction>     - Move to another room (north, south, east, west)")
        self.ui.print("  look               - Reprint the current room's description")

        self.ui.print("\nItem Interaction:")
        self.ui.print("  take <item>        - Pick up an item in the room")
        self.ui.print("  use <item>         - Use a misc or consumable item")
        self.ui.print("  equip <weapon>     - Equip a weapon from your backpack")
        self.ui.print("  inventory          - Show items you're carrying")
        self.ui.print("  inspect room       - List all items in the room")
        self.ui.print("  inspect <item>     - Examine an item in the room or in your backpack")

        self.ui.print("\nCombat:")
        self.ui.print("  fight              - Engage in combat with the monster here")

        self.ui.print("\nPuzzles:")
        self.ui.print("  solve              - Attempt to solve the room's puzzle")

        self.ui.print("\nSystem:")
        self.ui.print("  help               - Show this help message")
        self.ui.print("  quit               - Exit the game\n")

def main():
    """Main entry point for the game."""
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
