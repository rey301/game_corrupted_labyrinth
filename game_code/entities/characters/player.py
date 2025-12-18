from game_code.entities.character import Character
from game_code.entities.items.weapon import Weapon
from game_code.entities.items.med import Med


class Player(Character):
    """
    The user-controlled character, who can move through rooms,
    use items, pick up items and rewards, and engage combat with monsters.
    """

    def __init__(self, name, description, hp, max_hp, attack_power):
        super().__init__(name, description, hp, max_hp, attack_power)
        self.current_room = None
        self.storage = {}  # list of class Item
        self.weight = 0
        self.equipped_med = None
        self.max_weight = 64
        self.scannable = False  # when true the player can read logs
        self.equipped_weapon = None  # what weapon the player is currently holding

    def set_current_room(self, room):
        """
        Set the current room to where the player is moving to.
        :param room: The room the player moves to.
        :return: None
        """
        self.current_room = room

    def pick_up(self, item):
        """
        Pick up an item and add it to the player's storage.
        :param item: Item in which the player picks up.
        :return: True if the item has been picked up, otherwise False (too heavy).
        """
        # check the if the weight exceeds the storage capacity
        if (self.weight + item.weight) > self.max_weight:
            return False
        self.storage[item.name] = item
        self.weight += item.weight

        if item.name in self.current_room.items:
            self.current_room.remove_item(item)  # remove item from room

        return True

    def remove_item(self, item):
        """
        Removes a specified item from storage and drops it in the current room.
        If the player has an item equipped then it is unequipped first before removing it.
        :param item: The item that will be removed from storage
        :return: The string message updating the user on the storage capacity or the item wasn't found.
        """
        uses_flag = True
        lines = []
        if item.name in self.storage:
            # unequip anything that is equipped
            if self.equipped_weapon:
                if item.name == self.equipped_weapon.name:
                    lines.append(self.unequip(item))
            if self.equipped_med:
                if self.equipped_med.uses == 0:
                    uses_flag = False
                if item.name == self.equipped_med.name:
                    lines.append(self.unequip(item))

            # update weights and remove from storage
            item_weight = self.storage[item.name].weight
            prev_weight = self.weight
            self.weight -= item_weight
            self.storage.pop(item.name)
            if uses_flag:
                self.current_room.add_item(item)  # add the item to the room
            lines.append(
                f"{item.name} removed. \nCapacity updated: {prev_weight} - {item_weight} --> "
                f"{self.weight}/{self.max_weight} bytes.\n"
            )
            return "\n".join(lines)
        return "Item not found."

    def show_stats(self):
        """
        Showing the player's stats: HP, attack power, weight, and if the scan module is active.
        :return: The formatted string for the player's stats.
        """
        lines = [
            "[ PLAYER STATUS ]",
            f"Name: {self.name}",
            f"HP: {self.hp}/{self.max_hp}",
            f"Attack Power: {self.attack_power}",
            f"Storage Capacity: <{self.weight}/{self.max_weight}>",
            f"Scan Module Active: {'Yes' if self.scannable else 'No'}",
        ]
        return "\n".join(lines)

    def equip(self, item):
        """
        Equip a weapon or meds from the player's storage.
        :param item: Item to be equipped.
        :return: String message describing what was equipped.
        """
        # check the storage if item is inside
        if item.name not in self.storage:
            return f"You don't have {item.name}"

        stored_item = self.storage[item.name]

        # checking if item in storage is a weapon or med, then equip
        if isinstance(stored_item, Weapon):
            # equip the weapon
            self.equipped_weapon = stored_item
            self.attack_power = stored_item.damage

            return f"You equip {item.name}. Attack updated to {self.attack_power}."
        elif isinstance(stored_item, Med):
            self.equipped_med = stored_item
            return f"You equip {stored_item.name}. Uses updated to {stored_item.uses}."
        else:
            return f"You can't equip {stored_item.name}"

    def unequip(self, item):
        """
        Unequip an item from the player but keep it in storage.
        :return: String message describing what was unequipped.
        """
        if isinstance(item, Weapon):
            weapon_name = self.equipped_weapon.name
            self.equipped_weapon = None
            self.attack_power = 50
            return f"You unequip {weapon_name}. Attack updated to {self.attack_power}."
        if isinstance(item, Med):
            med_name = self.equipped_med.name
            self.equipped_med = None
            return f"You unequip {med_name}."
        else:
            return "Unknown type."
