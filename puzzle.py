class Puzzle:
    def __init__(self, prompt, solution, reward):
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