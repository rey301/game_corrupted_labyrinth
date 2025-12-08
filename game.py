"""
This class is the main class of the "Adventure World" application.
'Adventure World' is a very simple, text based adventure game. Users can walk
around some scenery. That's all. It should really be extended to make it more
interesting!

To play this game, create an instance of this class and call the "play" method.

This main class creates and initialises all the others: it creates all rooms,
creates the parser and starts the game. It also evaluates and executes the
commands that the parser returns.

This game is adapted from the 'World of Zuul' by Michael Kolling and 
David J. Barnes. The original was written in Java and has been simplified and
converted to Python by Kingsley Sage.
"""


from room import Room
from text_ui import TextUI


class Game:
    """Main class for the game."""

    def __init__(self):
        """
        Initialises the game.
        """
        self.create_rooms()
        self.current_room = self.outside
        self.ui = TextUI()

    def create_rooms(self):
        """
            Sets up all room assets.
        :return: None
        """
        self.outside = Room("You are outside")
        self.lobby = Room("in the lobby")
        self.corridor = Room("in a corridor")
        self.lab = Room("in a computing lab")
        self.office = Room("in the computing admin office")

        self.outside.set_exit("east", self.lobby)
        self.outside.set_exit("south", self.lab)
        self.outside.set_exit("west", self.corridor)
        self.lobby.set_exit("west", self.outside)
        self.corridor.set_exit("east", self.outside)
        self.lab.set_exit("north", self.outside)
        self.lab.set_exit("east", self.office)
        self.office.set_exit("west", self.lab)

    def play(self):
        """
            The main play loop.
        :return: None
        """
        self.print_welcome()
        finished = False
        while not finished:
            command = self.ui.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
        print("Thank you for playing!")

    def print_welcome(self):
        """
            Displays a welcome message.
        :return: None
        """
        self.ui.print("You are lost. You are alone. You wander around the deserted complex.")
        self.ui.print("")
        self.ui.print(f"Your command words are: {self.show_command_words()}")

    def show_command_words(self):
        """
            Show a list of available commands.
        :return: None
        """
        return ["help", "go", "quit"]

    def process_command(self, command):
        """
            Process a command from the TextUI.
        :param command: a 2-tuple of the form (command_word, second_word)
        :return: True if the game has been quit, False otherwise
        """
        command_word, second_word = command
        if command_word is not None:
            command_word = command_word.upper()

        want_to_quit = False
        if command_word == "HELP":
            self.print_help()
        elif command_word == "GO":
            self.do_go_command(second_word)
        elif command_word == "QUIT":
            want_to_quit = True
        else:
            # Unknown command...
            self.ui.print("Don't know what you mean.")

        return want_to_quit

    def print_help(self):
        """
            Display some useful help text.
        :return: None
        """
        self.ui.print("You are lost. You are alone. You wander around the deserted complex.")
        self.ui.print("")
        self.ui.print(f"Your command words are: {self.show_command_words()}.")

    def do_go_command(self, second_word):
        """
            Performs the GO command.
        :param second_word: the direction the player wishes to travel in
        :return: None
        """
        if second_word is None:
            # Missing second word...
            self.ui.print("Go where?")
            return

        next_room = self.current_room.get_exit(second_word)
        if next_room is None:
            self.ui.print("There is no door!")
        else:
            self.current_room = next_room
            self.ui.print(self.current_room.get_long_description())


def main():
    """Main entry point for the game."""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
