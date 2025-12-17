import unittest
from entities.characters.player import Player
from entities.characters.monster import Monster

class TestCombat(unittest.TestCase):
    def setUp(self):
        self.player = Player("Hero", "", 100, 100, 50)
        self.monster = Monster("Ant", "", hp=10, max_hp=10, attack_power=1, reward=None)

    def test_player_attack(self):
        self.player.attack(self.monster)
        self.assertEqual(self.monster.hp, 0)

    def test_monster_attack(self):
        self.monster.attack(self.player)
        self.assertEqual(self.player.hp, 99)

