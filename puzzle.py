from entity import Entity

class Puzzle(Entity):
    def __init__(self, name, prompt, solution, reward=None,  description=None):
        super().__init__(name, description)
        self.prompt = prompt
        self.solution = solution
        self.reward = reward
        self.solved = False

    def attempt(self, ui):
        """
        Checks if the player's solution solves the puzzle.
        :param ui: TextUI instance for input and output.
        :return: Message that summarises the result.
        """
        if self.solved:
            return "You have already solved this puzzle.", None

        ui.print(f"{self.name} opening...")
        ui.print(self.prompt)
        answer = ui.get_inp()# retrieve answer from user

        if answer == self.solution:
            self.solved = True
            ui.clear_logs()
            if self.reward:
                return "Engram has broken, it fizzles into air.", self.reward
        return "Incorrect. Try again.", None