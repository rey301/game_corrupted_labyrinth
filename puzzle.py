from entity import Entity
from item import Item

class Puzzle(Entity):
    def __init__(self, name, prompt, solution, reward,  description=None):
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
            return "You have already solved this puzzle."

        ui.print(self.prompt+"\n>")
        answer = ui.input()# retrieve answer from user

        if answer == self.solution:
            self.solved = True
            return "Puzzle has been solved."

        return "That doesn't seem correct."