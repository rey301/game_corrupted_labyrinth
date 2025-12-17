from entities.character import Character
from entities.items.weapon import Weapon
from entities.items.consumable import Consumable

class Player(Character):
    """
    The user-controlled characters, who can move through rooms,
    use items, pick up rewards, and engage in combat with monsters.
    """

    def __init__(self, name, description, hp, max_hp, attack_power):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.current_room = None
        self.storage = {} # list of class Item
        self.weight = 0
        self.equipped_med = None
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
        :param ui:
        :param item: Item in which the player picks up.
        :return: True if the item has been picked up, otherwise False (too heavy).
        """

        if (self.weight + item.weight) > self.max_weight:
            return False
        self.storage[item.name] = item
        self.weight += item.weight

        if item.name in self.current_room.items:
            self.current_room.remove_item(item) # remove item from room

        return True

    def remove_item(self, item):
        lines = []
        if item.name in self.storage:
            if self.equipped_weapon:
                if item.name == self.equipped_weapon.name:
                    lines.append(self.unequip(item))
            if self.equipped_med:
                if item.name == self.equipped_med.name:
                    lines.append(self.unequip(item))
            item_weight = self.storage[item.name].weight
            prev_weight = self.weight
            self.weight -= item_weight
            self.storage.pop(item.name)
            lines.append(
                f"{item.name} removed. \nCapacity updated: {prev_weight} - {item_weight} --> {self.weight}/{self.max_weight} bytes.\n")
            return "\n".join(lines)
        return "Item not found."

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
            "[ PLAYER STATUS ]",
            f"Name: {self.name}",
            f"HP: {self.hp}/{self.max_hp}",
            f"Attack Power: {self.attack_power}",
            f"Inventory Weight: {self.weight}/{self.max_weight}",
            f"Log Module Active: {'Yes' if self.scannable else 'No'}",
        ]
        return "\n".join(lines)

    def equip(self, item):
        """
        Equip a weapon or meds from the player's storage.
        :param item: String name of the weapon to equip.
        :return: String message describing what was equiped.
        """
        # check the storage if weapon is inside
        if item.name not in self.storage:
            return f"You don't have {item.name}"

        stored_item = self.storage[item.name]

        if isinstance(stored_item, Weapon):
            # equip the weapon
            self.equipped_weapon = stored_item
            self.attack_power = stored_item.damage

            return f"You equip {item.name}. Attack updated to {self.attack_power}."
        elif isinstance(stored_item, Consumable):
            self.equipped_med = stored_item
            return f"You equip {stored_item.name}. Uses updated to {stored_item.uses}"
        else:
            return f"You can't equip {stored_item.name}"

    def unequip(self, item):
        """
        Unequip a weapon from the player's storage.
        :return: String message describing what was unequipped.
        """
        if isinstance(item, Weapon):
            weapon_name = self.equipped_weapon.name
            self.equipped_weapon = None
            self.attack_power = 50
            return f"You unequip {weapon_name}. Attack updated to {self.attack_power}."
        if isinstance(item, Consumable):
            med_name = self.equipped_med.name
            self.equipped_med = None
            return f"You unequip {med_name}."
        else:
            return "Unknown type."

    def get_consumables(self):
        consumables = {}
        for item_name in self.storage:
            if isinstance(self.storage[item_name], Consumable):
                consumables[item_name] = self.storage[item_name]
        return consumables

class NotInStorageError(Exception):
    """A custom exception to handle items not in backpack."""
    def __init__(self, item, message):
        print(f'{item} {message}')
