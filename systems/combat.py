from random import random

class Combat:
    ESCAPE_CHANCE = 0.6

    def __init__(self, ui, player, monster):
        self.ui = ui
        self.player = player
        self.monster = monster

    def start(self):
        """Runs the combat loop. Returns True if player wins, False if player dies/retreats."""
        self._display_start()

        while self.player.is_alive() and self.monster.is_alive():
            action = self._get_action()
            self.ui.clear_logs()

            if action == "retreat":
                if self._attempt_retreat(): return "retreat"
                continue
            elif action == "heal":
                self._handle_heal()
            elif action == "attack":
                self._execute_player_attack()

            if self.monster.is_alive():
                self._execute_monster_attack()

            self.ui.print(f"{self.monster.name} HP: {self.monster.hp}/{self.monster.max_hp}")
            self.ui.print(f"Your HP: {self.player.hp}/{self.player.max_hp}")
        return None

    def _display_start(self):
        self.ui.print(f"You engage the {self.monster.name}")
        self.ui.print(f"{self.monster.name} HP: {self.monster.hp}/{self.monster.max_hp}")
        self.ui.print(f"Your HP: {self.player.hp}/{self.player.max_hp}")

    def _get_action(self):
        self.ui.print("\nChoose your action:")
        self.ui.print("[1] Attack\n[2] Heal\n[3] Retreat")

        while True:
            key = self.ui.get_key()
            if key == "1": return "attack"
            if key == "2": return "heal"
            if key == "3": return "retreat"
            if key == -1: continue

    def _execute_player_attack(self):
        dmg = self.player.attack(self.monster)
        w_name = self.player.equipped_weapon.name if self.player.equipped_weapon else "fists"
        self.ui.print(f"You strike with {w_name} for {dmg}")

    def _execute_monster_attack(self):
        dmg = self.monster.attack(self.player)
        self.ui.print(f"{self.monster.name} hits you for {dmg}!")
        self.ui.draw_hud(self.player)

    def _attempt_retreat(self):
        if random() < self.ESCAPE_CHANCE:
            self.ui.print(f"You escaped! {self.monster.name} growls in frustration.")
            return True
        self.ui.print("Escape failed!")
        self._execute_monster_attack()
        return False

    def _handle_heal(self):
        # Logic from your heal_player goes here
        pass