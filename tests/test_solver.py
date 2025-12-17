import unittest

from entities.room import Room
from systems.solver import Solver
from entities.puzzle import Puzzle
from entities.characters.player import Player

class TestSolver(unittest.TestCase):
    def setUp(self):
        self.puzzle = Puzzle(
            name="Test Puzzle",
            prompt="What is 2+2?",
            solution="4",
            reward=None
        )
        self.player = Player("Test","", 100,100,20)
        self.solver = Solver(ui=None, player=self.player)
        self.room = Room("test_room", "")
        self.room.puzzle = self.puzzle
        self.player.set_current_room(self.room)

    def test_solve(self):
        self.assertTrue(self.solver.check_solution("4"))
        self.assertFalse(self.solver.check_solution("2"))