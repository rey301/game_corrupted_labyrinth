import unittest

from game_code.entities.characters.player import Player
from game_code.entities.items.weapon import Weapon
from game_code.entities.room import Room
from game_code.systems.storage_handler import StorageHandler


class TestInventory(unittest.TestCase):
    """
    This tests if picking up an item is valid (checking weights).
    """
    def setUp(self):
        self.player = Player("Test", "", 100, 100, 50)
        self.inventory = StorageHandler(None, None)  # UI & Game not needed
        self.room = Room("Test_room", "")
        self.player.set_current_room(self.room)


    def test_pick_up_within_capacity(self):
        self.weapon = Weapon("Knife", "", weight=5, damage=3)
        self.room.add_item(self.weapon)
        self.assertTrue(self.player.pick_up(self.weapon))

    def test_pick_up_over_capacity(self):
        self.weapon = Weapon("Knife", "", weight=100, damage=3)
        self.room.add_item(self.weapon)
        self.assertFalse(self.player.pick_up(self.weapon))