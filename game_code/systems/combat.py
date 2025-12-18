from random import random
import time

from game_code.entities.items.med import Med
from game_code.entities.items.weapon import Weapon


class Combat:
    """
    This class allows a player to engage in combat with a monster.
    It features a turn-based combat a player can choose to attack the monster, heal themselves, or escape
    (where they only have a 60% chance of escaping).
    If the player dies, the game is over and if the monster dies, the player receives their reward (if the monster
    has one)
    """
    ESCAPE_CHANCE = 0.6

    def __init__(self, ui, player, monster, game):
        self.ui = ui
        self.player = player
        self.monster = monster
        self.game = game

    def start(self):
        """
        Runs the combat loop in which the player can choose an action every turn.
        :return: string "retreat" if the player is able to leave the combat early otherwise None.
        """
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
        """
        This displays the string messsage for the combat start.
        :return: None
        """
        self.ui.clear_logs()
        self.ui.display_text(f"You engage the {self.monster.name}")
        self.ui.display_text(f"{self.monster.name} HP: {self.monster.hp}/{self.monster.max_hp}")
        self.ui.display_text(f"Your HP: {self.player.hp}/{self.player.max_hp}")

    def get_action(self):
        """
        This allows the user to choose an action according to the three options.
        :return: The string message action that the user chooses.
        """
        self.ui.display_text("\nChoose your action:")
        self.ui.display_text("[1] Attack\n[2] Heal\n[3] Retreat")

        while True:
            key = self.ui.wait_for_key()
            if key == "1": return "attack"
            if key == "2": return "heal"
            if key == "3": return "retreat"
            if key == -1: continue

    def execute_player_attack(self):
        """
        Player attacks the monster in the combat loop and displays the damage given.
        :return: None
        """
        dmg = self.player.attack(self.monster)
        w_name = self.player.equipped_weapon.name if self.player.equipped_weapon else "fists"
        self.ui.display_text(f"You strike with {w_name} for {dmg}")

    def execute_monster_attack(self):
        """
        Monster attack the player in the combat loop and displays the damage given.
        :return:
        """
        dmg = self.monster.attack(self.player)
        self.ui.display_text(f"{self.monster.name} hits you for {dmg}!")
        self.ui.draw_hud(self.player)

    def attempt_retreat(self):
        """
        Using the constant ESCAPE_CHANCE, the player attempts to retreat with a 60% chance.
        :return: True if the escape happens, False otherwise.
        """
        if random() < self.ESCAPE_CHANCE:
            self.ui.display_text(f"You escaped! {self.monster.name} growls in frustration.")
            return True
        self.ui.display_text("Escape failed!")
        self.execute_monster_attack()
        return False

    def handle_combat_end(self, monster, room):
        """
        Handle combat where if the player dies, the game is over or if the monster dies,
        the reward is given to the player.
        :return: None
        """
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
        """
        Checks if the monster has a reward, and if so, allow the player to pick up the reward. If it isn't picked up,
        then the item falls to the floor and is added to the room items.
        :return: None
        """
        if not monster.reward:
            return

        self.ui.display_text(f"You have received: {monster.reward.name}\n")
        prev_weight = self.player.weight
        picked_up = self.player.pick_up(monster.reward)

        if not picked_up:
            self.ui.display_text(f"{monster.reward.name} is too heavy to carry.")
        elif picked_up:
            self.ui.display_text(f"{monster.reward.name} added to storage.")
            self.ui.display_text(f"Storage: {prev_weight} + {monster.reward.weight} --> "
                                 f"{self.player.weight}/{self.player.max_weight} bytes")
            time.sleep(1)
            self.ui.clear_logs()

            prompt_msg = None
            if isinstance(monster.reward, Weapon) and monster.reward.damage > self.player.attack_power:
                prompt_msg = f"{monster.reward.name} is stronger than your current attack power. Equip?"

            elif isinstance(monster.reward, Med) and self.player.equipped_med is None:
                prompt_msg = "You don't have any meds currently equipped. Equip?"

            if prompt_msg:
                self.ui.display_text(prompt_msg)
                self.ui.display_text("[1] Yes\n[2] No")

                while True:
                    key = self.ui.wait_for_key()
                    if key == -1: continue

                    if key == "1":
                        msg = self.player.equip(monster.reward)
                        self.ui.clear_logs()
                        self.ui.display_text(msg)
                        logging.info(f"Player equipped {monster.reward.name}")
                        break
                    elif key == "2":
                        self.ui.clear_logs()
                        break


