from character import Character
from weapon import Weapon
from consumable import Consumable

class Player(Character):
    """
    The user-controlled character, who can move through rooms,
    use items, pick up rewards, and engage in combat with monsters.
    """

    def __init__(self, name, description, hp, max_hp, attack_power):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.current_room = None
        self.storage = {} # list of class Item
        self.weight = 0
        self.max_weight = 64
        self.scannable = False # when true the player can read logs
        self.equipped_weapon = None # what weapon the player is currently holding

    def set_current_room(self, room):
        """
        Set the room to the current room that the player is in.
        :param room: The room the player moves to.
        :return: None
        """
        self.current_room = room

    def pick_up(self, item):
        """
            Pick up an item and add to storage, checking the weight limit before
            pick up.
        :param item: Item in which the player picks up.
        :return: True if the item has been picked up, otherwise False (too heavy).
        """

        if (self.weight + item.weight) > self.max_weight:
            return False
        self.storage[item.name] = item
        self.weight += item.weight
        return True

    def use(self, item):
        """
            Use a chosen item and.
        :param item: Item in which the player has in their backpack.
        """

    def show_storage(self):
        """
            Displays the storage.
        :return: The string content of the player's backpack.
        """
        if self.weight == 0:
            return "Your storage is empty."

        res = ["Your storage contains: \n"]
        for name, item in self.storage.items():
            res.append(f"- {name} (Weight: {item.weight})")
        res.append(f"\nCapacity: {self.weight}/{self.max_weight} bytes")
        return "\n".join(res)

    def remove_item(self, item_name):
        item_weight = self.storage[item_name].weight
        prev_weight = self.weight
        self.weight -= item_weight
        self.storage.pop(item_name)
        return f"{item_name} deleted. \nCapacity updated: {prev_weight} - {item_weight} --> {self.weight}/{self.max_weight} bytes"

    def is_alive(self):
        """
            Checks if the player's hp is 0.
        :return: True if player has hp > 0, False otherwise.
        """
        if self.hp == 0:
            return False
        else:
            return True

    def show_stats(self):
        """
        Showing the player's stats, with hp and attack power.
        :return: The formatted string for the player's stats.
        """
        lines = [
            "=== PLAYER STATUS ===",
            f"Name: {self.name}",
            f"HP: {self.hp}/{self.max_hp}",
            f"Attack Power: {self.attack_power}",
            f"Inventory Weight: {self.weight}/{self.max_weight}",
            f"Log Module Active: {'Yes' if self.scannable else 'No'}",
        ]
        return "\n".join(lines)

    def equip(self, weapon_name):
        """
        Equip a weapon from the player's storage.
        :param weapon_name: String name of the weapon to equip.
        :return: String message describing what was equiped.
        """
        # check the storage if weapon is inside
        if weapon_name not in self.storage:
            return f"You don't have {weapon_name}"

        item = self.storage[weapon_name]

        # check if it's a weapon
        if not isinstance(item, Weapon):
            return f"You can't equip {weapon_name}"

        # equip the weapon
        self.equipped_weapon = item
        self.attack_power = item.damage

        return f"You equip {item.name}. Attack power has been updated to {self.attack_power}."

    def get_consumables(self):
        consumables = {}
        for item in self.storage:
            if isinstance(self.storage[item], Consumable):
                consumables[item] = item
        return consumables

class NotInStorageError(Exception):
    """A custom exception to handle items not in backpack."""
    def __init__(self, item, message):
        print(f'{item} {message}')
