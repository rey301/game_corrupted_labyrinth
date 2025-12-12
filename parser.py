from command import Command

class Parser:
    def __init__(self, ui):
        self.ui = ui
        self.valid_verbs = {
            "go", "take", "use", "fight", "solve", "inspect",
            "help", "quit"
        }

    def get_command(self):
        """
        Takes user input using the TextUI and converts it
        to a structure Command object (verb, obj).
        Splits the input into a verb and optional object argument.
        :return: A command object containing (verb, obj).
        """
        verb = None
        obj = None
        inp = self.ui.input("> ").strip().lower()

        if inp != "":
            all_words = inp.split()
            verb = all_words[0]
            if len(all_words) > 1:
                obj = all_words[1]
            else:
                obj = None
            # Just ignore any other words
        return Command(verb, obj)

    def get_key(self):
        pass

