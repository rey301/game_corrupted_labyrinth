from random import random
import time

class Combat:
    ESCAPE_CHANCE = 0.6

    def __init__(self, ui, player, monster, game):
        self.ui = ui
        self.player = player
        self.monster = monster
        self.game = game

    def start(self):
        """Runs the combat loop. Returns True if player wins, False if player dies/retreats."""
        self.display_start()

        while self.player.is_alive() and self.monster.is_alive():
            healed = True
            action = self.get_action()
            self.ui.clear_logs()

            if action == "retreat":
                if self.attempt_retreat(): return "retreat"
                continue
            elif action == "heal":
                healed = self.game.heal_player()
            elif action == "attack":
                self.execute_player_attack()

            if self.monster.is_alive() and healed:
                self.execute_monster_attack()

            self.ui.display_text(f"{self.monster.name} HP: {self.monster.hp}/{self.monster.max_hp}")
            self.ui.display_text(f"Your HP: {self.player.hp}/{self.player.max_hp}")

        self.handle_combat_end(self.monster, self.player.current_room)
        return None

    def display_start(self):
        self.ui.clear_logs()
        self.ui.display_text(f"You engage the {self.monster.name}")
        self.ui.display_text(f"{self.monster.name} HP: {self.monster.hp}/{self.monster.max_hp}")
        self.ui.display_text(f"Your HP: {self.player.hp}/{self.player.max_hp}")

    def get_action(self):
        self.ui.display_text("\nChoose your action:")
        self.ui.display_text("[1] Attack\n[2] Heal\n[3] Retreat")

        while True:
            key = self.ui.get_key()
            if key == "1": return "attack"
            if key == "2": return "heal"
            if key == "3": return "retreat"
            if key == -1: continue

    def execute_player_attack(self):
        dmg = self.player.attack(self.monster)
        w_name = self.player.equipped_weapon.name if self.player.equipped_weapon else "fists"
        self.ui.display_text(f"You strike with {w_name} for {dmg}")

    def execute_monster_attack(self):
        dmg = self.monster.attack(self.player)
        self.ui.display_text(f"{self.monster.name} hits you for {dmg}!")
        self.ui.draw_hud(self.player)

    def attempt_retreat(self):
        if random() < self.ESCAPE_CHANCE:
            self.ui.display_text(f"You escaped! {self.monster.name} growls in frustration.")
            return True
        self.ui.display_text("Escape failed!")
        self.execute_monster_attack()
        return False

    def handle_combat_end(self, monster, room):
        """Handle post-combat rewards and consequences."""
        time.sleep(2)
        self.ui.clear_logs()

        if monster.hp == 0:
            self.ui.display_text(f"{monster.name} has fallen.")
            self.handle_monster_reward(monster, room)
            room.remove_monster(monster)

        if self.player.hp == 0:
            self.ui.clear_logs()
            self.ui.display_text("The pixels fade to black...")
            self.game.game_over = True
            time.sleep(3)

    def handle_monster_reward(self, monster, room):
        """Handle monster reward drops."""
        if not monster.reward:
            return

        self.ui.display_text(f"You have received: {monster.reward.name}\n")
        msg, picked_up = self.player.pick_up(monster.reward, self.ui)
        self.ui.display_text(msg)

        if not picked_up:
            room.add_item(monster.reward)
            self.ui.display_text(f"{monster.reward.name} has fallen to the floor.")