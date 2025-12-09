from entity import Entity
from item import Item

class Puzzle(Entity):
    def __init__(self, name, prompt, solution, reward,  description=None):
        super().__init__(name, description)
        self.prompt = prompt
        self.solution = solution
        self.reward = reward
        self.solved = False

    def attempt(self, ans):
        """
            Checks if the player's solution solves the puzzle.
        :param ans: Player's attempted solution.
        :return: True if solved, False otherwise.
        """