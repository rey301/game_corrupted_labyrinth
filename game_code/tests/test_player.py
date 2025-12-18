import unittest

from game_code.entities.characters.player import Player
from game_code.entities.items.med import Med
from game_code.entities.items.weapon import Weapon
from game_code.entities.room import Room


class TestPlayer(unittest.TestCase):
    """
    This test checks for HP changes, equipping and unequipping behaviour, and the storage capacity.
    """
    def setUp(self):
        self.player = Player("Test", "", hp=50, max_hp=100, attack_power=50)
        self.med = Med("test_med", "healing!!", weight=2, heal=30, uses=1, max_uses=1)
        self.weapon = Weapon("Knife", "sharp!!!", weight=3, damage=5)
        self.test_room = Room("test_room", "")
        self.test_room.add_item(self.weapon)
        self.test_room.add_item(self.med)
        self.player.set_current_room(self.test_room)

    def test_player_heal(self):
        self.player.equipped_med = self.med
        msg, flag = self.med.use(self.player)

        self.assertEqual(self.player.hp, 80)
        self.assertEqual(flag, "remove") # only 1 use left

    def test_equip_weapon(self):
        self.player.pick_up(self.weapon)
        self.player.equip(self.weapon)

        self.assertEqual(self.player.attack_power, 5) # attack power updated to 5
        self.assertEqual(self.player.equipped_weapon, self.weapon) # weapon is equipped
        self.assertEqual(self.player.weight, 3) # weight of weapon added to player

    def test_unequip_weapon(self):
        self.player.pick_up(self.weapon)
        self.player.equip(self.weapon)
        self.player.unequip(self.weapon)

        self.assertEqual(self.player.attack_power, 50) # attack power updated back to 50
        self.assertEqual(self.player.equipped_weapon, None) # weapon is unequipped
        self.assertEqual(self.player.weight, 3) # weight of player still 3 as it's not removed from storage

    def test_equip_med(self):
        self.player.pick_up(self.med)
        self.player.equip(self.med)

        self.assertEqual(self.player.equipped_med, self.med)  # med is equipped
        self.assertEqual(self.player.weight, 2)  # weight of med added to player

    def test_unequip_med(self):
        self.player.pick_up(self.med)
        self.player.equip(self.med)
        self.player.unequip(self.med)

        self.assertEqual(self.player.equipped_med, None) # med is unequipped
        self.assertEqual(self.player.weight, 2) # weight of player still 2 as it's not removed from storage

    def test_is_alive(self):
        self.assertTrue(self.player.is_alive())
        self.player.hp = 0
        self.assertFalse(self.player.is_alive())
