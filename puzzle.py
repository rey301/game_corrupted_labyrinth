from entity import Entity

class Puzzle(Entity):
    def __init__(self, name, prompt, solution, reward=None,  description=None):
        super().__init__(name, description)
        self.prompt = prompt
        self.solution = solution
        self.reward = reward
        self.solved = False