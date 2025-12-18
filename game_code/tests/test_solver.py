import unittest

from game_code.entities.characters.player import Player
from game_code.entities.puzzle import Puzzle
from game_code.entities.room import Room
from game_code.systems.puzzle_handler import PuzzleHandler


class TestSolver(unittest.TestCase):
    def setUp(self):
        self.puzzle = Puzzle(
            name="Test Puzzle",
            prompt="What is 2+2?",
            solution="4",
            reward=None
        )
        self.player = Player("Test","", 100,100,20)
        self.solver = PuzzleHandler(ui=None, player=self.player, game=None)
        self.room = Room("test_room", "")
        self.room.puzzle = self.puzzle
        self.player.set_current_room(self.room)

    def test_solve(self):
        self.assertTrue(self.solver.check_solution("4"))
        self.assertFalse(self.solver.check_solution("2"))