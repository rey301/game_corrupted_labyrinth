from entities.items.consumable import Consumable
from entities.items.weapon import Weapon


class Inventory:
    def __init__(self, ui, game):
        self.ui = ui
        self.game = game

    def show_player_storage(self):
        """Display player's inventory with item selection."""
        storage = self.game.player.storage

        if not storage:
            self.ui.display_text("Your storage is empty.")
            return

        selections = {}
        self.ui.display_text("[ STORAGE ]\n")

        for i, (name, item) in enumerate(storage.items(), start=1):
            self.ui.display_text(f"[{i}] {name} (W:{item.weight})")
            selections[str(i)] = item

        self.ui.display_text("[B] Back")
        self.ui.display_text(f"\n[ CAP <{self.game.player.weight}/{self.game.player.max_weight}> ]")

        key = self.game.menu.wait_for_key()

        if key == "ESC":
            self.game.menu.pause()

        # Check for valid item selection
        if key in selections:
            self.inspect_item(selections[key])
            return  # Exit menu after inspecting

        # Check for Exit command
        if key == "b":
            self.ui.clear_logs()
            return

    def inspect_item(self, item):
        """Display item details and available actions."""
        self.ui.clear_logs()

        self.ui.display_text(f"[ {item.name} ]")
        self.ui.display_text(f"{item.description}\n")

        actions = self.get_item_actions(item)

        for action_key, label, _ in actions:
            self.ui.display_text(f"[{action_key}] {label}")
        self.ui.display_text("[B] Back")

        user_key = self.game.menu.wait_for_key()

        if user_key == "ESC":
            self.game.menu.pause()

        for action_key, _, action in actions:
            if user_key == action_key:
                self.ui.clear_logs()
                msg = action()
                if msg:
                    self.ui.display_text(msg)
                return
            # Check for Exit command
            if user_key == "b":
                self.ui.clear_logs()
                self.show_player_storage()
                return

    def get_item_actions(self, item):
        """Get available actions for an item based on its type."""
        player = self.game.player
        actions = []

        if isinstance(item, Weapon):
            is_equipped = player.equipped_weapon == item
            actions.append((
                "1",
                "Unequip" if is_equipped else "Equip",
                lambda: player.unequip(item) if is_equipped else player.equip(item)
            ))
            actions.append(("2", "Drop", lambda: self.game.do_drop(item)))

        elif isinstance(item, Consumable):
            is_equipped = player.equipped_med == item
            actions.append((
                "1",
                "Unequip" if is_equipped else "Equip",
                lambda: player.unequip(item) if is_equipped else player.equip(item)
            ))
            actions.append(("2", "Use", lambda: self.game.heal_player()))
            actions.append(("3", "Drop", lambda: self.game.do_drop(item)))

        else:  # Misc items
            actions.append(("1", "Use", lambda: self.game.do_use(item)))
            actions.append(("2", "Drop", lambda: self.game.do_drop(item)))

        return actions