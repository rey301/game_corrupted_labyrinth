from entities.entity import Entity


class Puzzle(Entity):
    """
    A puzzle placed in specific rooms in the game in which the player can solve and receive rewards from.
    """
    def __init__(self, name, prompt, solution, reward=None, description=None):
        super().__init__(name, description)
        self.prompt = prompt
        self.solution = solution
        self.reward = reward
        self.solved = False
