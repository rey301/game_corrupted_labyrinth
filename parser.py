from command import Command

class Parser:
    def get_command(self, inp):
        """
Takes user input using the TextUI and converts it
to a structure Command object (verb, obj).
Splits the input into a verb and optional object argument.
:return: A command object containing (verb, obj).
        """
        verb = None
        obj = None
        if inp != "":
            all_words = inp.split()
            verb = all_words[0]
            if len(all_words) > 1:
                obj = all_words[1]
            else:
                obj = None
            # Just ignore any other words
        return (verb, obj)

