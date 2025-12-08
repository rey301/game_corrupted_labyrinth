from player import Player
from game_code.parser import Parser
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
        self.game_over = False

    def play(self):
        """
            The main play loop that displays welcome message, reads player input
            in a loop, processes commands, and terminates when game_over becomes
            True.
        :return: None
        """
        self.print_welcome()
        finished = False
        while not finished:
            command = self.ui.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
        print("Thank you for playing!")

    def process(self, cmd):
        """
            Handles user commands and invokes an action method from
            the command given (e.g. item interaction, problem solving).
        :param cmd: Parse command object containing the verb and obj (optional)
        :return: True if game should end (quit or player dies), otherwise False if game continues
        """

    def do_go(self, dir):
        """
            Move player into room given the direction, and if exit doesn't exist;
            error message is displayed.
        :param dir: Direction the player wishes to move (e.g. north, east)
        """

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
