from player import Player
from parser import Parser
from world_builder import WorldBuilder
from text_ui import TextUI

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

        self.player = Player()
        self.parser = Parser()
        self.ui = TextUI()
        self.world = WorldBuilder()
        self.world.build()
        self.game_over = False

    def play(self):
        """
            The main play loop that displays welcome message, reads player input
            in a loop, processes commands, and terminates when game_over becomes
            True.
        :return: None
        """
        # intialise world and intro messages
        start_room = self.world.build()
        self.ui.print("Welcome to the Labyrinth. \nType HELP to see available commands.\n")
        self.player.current_room.describe()

        # main game loop
        while not self.game_over and self.player.is_alive():
            input = self.ui.input()
            command = self.parser.get_command(input)
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

    def do_take(self, item_name):
        """
        Attempt to pick up an item from the current room and put it in the
        player's backpack.
        :param item_name: Name of the item the player wishes to pick up.
        :return: None
        """

    def do_use(self, item_name):
        """
            Allows player to use an item from their backpack, applying whatever
            effect the item has.
        :param item_name: Name of the item to use.
        :return: None
        """

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

def main():
    """Main entry point for the game."""
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
