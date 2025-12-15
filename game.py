from player import Player
import curses
from parser import Parser
from world_builder import WorldBuilder
from text_ui import TextUI
from weapon import Weapon
from consumable import Consumable
from misc import Misc
import time

class Game:
    """
        The main controller for the game, which manages the play() state,
        user commands, and coordinates interactions between the player,
        world, and UI. Parsing for commands is taken to the Parser,
        constructing the game world/map is done to the WorldBuilder,
        and user input/output to the TextUI.
    """

    def __init__(self):
        """
        Initialises the game.
        """

        self.player = Player("Lapel","",500, 500, 50)
        #self.parser = Parser(self.ui)
        self.ui = TextUI()
        self.world = WorldBuilder()
        self.game_over = False

    def run(self):
        """
        Entry point for the game.
        Handles UI lifecycle safely.
        """
        self.ui.start()
        try:
            self.play()
            if self.game_over:
                if not self.player.is_alive():
                    choice = self.game_over_menu()
                    return choice
            return "quit"
        finally:
            self.ui.stop()

    def play(self):
        """
            The main play loop that generates the world, displays welcome message, reads player input
            in a loop, processes commands, and terminates when game_over becomes
            True.
        :return: None
        """
        # initialise world and intro messages
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.print("""
> INITIALISING SESSION...
> LOADING USER MEMORY.............FAILED
> CHECKSUM ERROR IN SECTOR 0

[ WARNING ]
Your consciousness has been loaded into an unstable system.

Fragments of memory are missing.
Paths are corrupted.
Something hostile is running in the background.

You don’t remember how you got here.
You don’t remember who you were.

You only know one thing:
YOU MUST REACH THE KERNEL
AND ESCAPE BEFORE THE SYSTEM COLLAPSES""")
        time.sleep(5)
        self.ui.draw_room(self.player.current_room.describe())
        self.ui.draw_hud(self.player)
        time.sleep(2)
        self.ui.print("Press '/' for available commands.")

        # main game loop
        while not self.game_over and self.player.is_alive():
            key = self.ui.get_key()
            self.handle_key(key)

    def game_over_menu(self):
        text = (
            "=== SYSTEM FAILURE ===\n"
            "You have been terminated.\n\n"
            "[R] Restart\n"
            "[Q] Quit"
        )
        self.ui.draw_top(text)

        while True:
            key = self.ui.get_key().lower()
            if key == "r":
                return "restart"
            elif key == "q":
                return "quit"

    def pause_menu(self):
        self.ui.draw_top(
            "=== SYSTEM PAUSED ===\n\n"
            "[ESC] Resume\n"
            "[R] Restart\n"
            "[Q] Quit",
        )

        while True:
            key = self.ui.get_key()

            if key == "ESC":
                self.ui.redraw_game(self.player.current_room, self.player)  # redraw room + HUD
                return

            elif key == "r":
                self.player = Player("Lapel", "", 500, 500, 50)
                start_room = self.world.build()
                self.player.set_current_room(start_room)
                self.ui.clear()
                self.ui.redraw_game(self.player.current_room, self.player)
                return

            elif key == "q":
                self.game_over = True
                return

    def handle_key(self, key):
        self.ui.clear_logs()
        # movement
        if key == curses.KEY_UP:
            self.move("north")
        elif key == curses.KEY_DOWN:
            self.move("south")
        elif key == curses.KEY_LEFT:
            self.move("west")
        elif key == curses.KEY_RIGHT:
            self.move("east")

        # scanning room for entities
        elif key == "r":
            self.scan_room()

        elif key == "p":
            self.do_solve()

        # list items in room and allow user to select an item to take
        elif key == 't':
            self.take_item()

        elif key == 'h':
            self.heal_player()

        elif key == 's':
            self.show_player_storage()

        elif key == 'i':
            self.ui.print(self.player.show_stats())

        elif key == '/':
            self.print_help()

        elif key == "ESC":
            self.pause_menu()
            return
        else:
            self.ui.print("Unknown command.")
        self.ui.draw_hud(self.player)

    def move(self, direction):
        """
        Move player into room given the direction, and if exit doesn't exist;
        error message is displayed.
        :param direction: Direction the player wishes to move (e.g. north, east)
        """
        room = self.player.current_room
        self.ui.clear_logs()

        if direction not in room.exits:
            self.ui.print("You can't go that way!")
            return

        next_room = room.get_exit(direction)

        # checking if a monster blocks an exit
        for m in room.monsters.values():
            if m.blocks_exit == direction:
                self.ui.clear_logs()
                self.ui.print(f"{m.name} has blocked you!")
                self.ui.print("Defeating it is the only way in...")
                self.do_fight(m.name)
                return

        # check for locks
        if direction in room.locked_exits:
            lock_id = room.locked_exits[direction]
            self.ui.print(f"The path to {next_room.name} is locked ({lock_id})")

            # check if player has the key
            key_item = None
            for item in self.player.storage.values():
                if isinstance(item, Misc) and item.misc_id == lock_id:
                    key_item = item
                    break

            if key_item:
                self.ui.clear_logs()
                self.ui.print(f"Use {key_item.name} to unlock?")
                self.ui.print("\n[1] Yes\n[2] No")

                key = self.ui.get_key()
                self.ui.clear_logs()
                if key == "1":
                    if room.name == "obsolete_hub" and not room.kernel_unlock:
                        self.ui.print("You need the activate the decrypter.")
                    else:
                        # use the item
                        self.do_use(key_item)
                        self.player.current_room = next_room
                        self.ui.draw_room(self.player.current_room.describe())


                    return
            return

        if next_room is not None:
            self.player.current_room = next_room
            self.ui.clear()
            self.ui.draw_room(self.player.current_room.describe())
            return


    def scan_room(self):
        """
        Inspect an object which could be an item, a monster, a puzzle, or the whole room.
        :param obj: This is the object that the user defines (e.g. item name)
        :return: None
        """
        # inspect the room for everything
        room = self.player.current_room

        # If the room contains nothing of interest
        if not room.items and not room.monsters and not room.puzzle:
            self.ui.print("The room reveals nothing unusual.")
            return

        lines = ["Scanning...\n"]

        # items
        if room.items:
            lines.append("[ Items Detected ]")
            for item_name, item in room.items.items():
                lines.append(f" - {item_name}")
            lines.append("")  # blank line
        else:
            lines.append("[ No Items Detected ]\n")

            # monsters
        if room.monsters:
            lines.append("[ Hostile Entities ]")
            for monster in room.monsters:
                lines.append(f" - {room.monsters[monster].name}")
            lines.append("")
        else:
            lines.append("[ No Hostiles Present ]\n")

        # puzzle
        if room.puzzle:
            puzzle = room.puzzle
            lines.append("[ Corrupted Engram Detected ]")
            lines.append(f" - {puzzle.name}\n")

        # check if user has the phantom key
        if "phantom_key" in self.player.storage:
            lines.append("[ Spatial Anomaly Detected ]")
            lines.append("A faint doorway signature is flickering here...\n")

        self.ui.print("\n".join(lines))
        return

    def take_item(self):
        """
        Attempt to pick up an item from the current room and put it in the
        player's backpack.
        :param item_name: Name of the item the player wishes to pick up.
        :return: None
        """
        room = self.player.current_room
        item_count = 1
        selections = {}

        if not bool(room.items):
            self.ui.print("There are no items to pick up.")
            return
        else:
            self.ui.print("Pick an item:")
            for item_name in room.items:
                self.ui.print(f"[{str(item_count)}] {item_name}")
                selections[str(item_count)] = room.items[item_name]
                item_count += 1

            key = self.ui.get_key()
            if key in selections:
                self.ui.clear_logs()
                chosen_item = selections[key]
                msg, flag = self.player.pick_up(chosen_item, self.ui)
                self.ui.print(msg)
            return

    def heal_player(self):
        if self.player.equipped_med:
            med = self.player.equipped_med
            if self.player.hp == self.player.max_hp:
                self.ui.print("You are at max hp!")
            else:
                msg, flag = med.use(self.player)
                self.ui.print(f"You use {med.name}. {msg}")
                if flag == "remove":
                    self.ui.print("Med charges depleted!")
                    self.ui.print(self.player.remove_item(med))
        else:
            self.ui.print("You don't have any meds equipped!")
        return

    def drop_items(self):
        room = self.player.current_room
        item_count = 1
        selections = {}

        if not bool(self.player.storage):
            self.ui.print("Your storage is empty.")
        else:
            self.ui.print("Pick an item to drop:")
            for item_name in self.player.storage:
                self.ui.print(f"[{str(item_count)}] {item_name}")
                selections[str(item_count)] = self.player.storage[item_name]
                item_count += 1

            key = self.ui.get_key()
            if key in selections:
                chosen_item = selections[key]
                msg = self.player.remove_item(chosen_item)
                self.ui.clear_logs()
                self.ui.print(msg)
                room.add_item(chosen_item)
                self.ui.print(f"{chosen_item.name} has fallen to the floor.")
        return

    def do_drop(self, item):
        """
        Select an item to drop from player's storage and is place in the room.
        :param item_name: The item the player wishes to drop.
        :return: None
        """
        room = self.player.current_room

        if item.name is None:
            self.ui.print("Drop what?")
            return

        if item.name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        # remove from storage
        self.ui.print(self.player.remove_item(item))

        # add item to room
        room.add_item(item)

        self.ui.print(f"{item.name} has fallen to the floor.")

    def do_use(self, item):
        """
        Allows player to use an item from their backpack, applying whatever
        effect the item has.
        :param item_name: Name of the item to use.
        :return: None
        """
        if item.name is None:
            self.ui.print("Use what?")
            return

        if item.name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        # check if it's a weapon
        if isinstance(item, Weapon):
            self.ui.print(f"You can't 'use' {item.name}. Try 'equip {item.name}' instead.")
            return

        # for healing
        if isinstance(item, Consumable):
            if self.player.hp == self.player.max_hp:
                self.ui.print("You are at max hp!")
            else:
                healed, flag = item.use(self.player)
                self.ui.print(f"You use {item.name}. {healed}")
                msg = self.player.remove_item(item.name)
                self.ui.print(msg)
            return

        # for unlocking something
        if isinstance(item, Misc):
            result, flag = item.use(self.player, self.player.current_room, self.world)

            if result:
                self.ui.print(result)
                if flag == "remove":
                    self.ui.print(self.player.remove_item(item))
            else:
                self.ui.print(f"You can't use {item} here.")
            return

        self.ui.print("Nothing happens.")

    def do_equip(self, weapon_name):
        if weapon_name is None:
            self.ui.print("Equip what?")
            return

        self.ui.print(self.player.equip(weapon_name))

    def do_fight(self, monster_name):
        """
        Handles the combat with a monster in the current room, where combat
        alternates between player and the monster until one is defeated.
        Game is over if the player dies. If the monster dies, the player
        is rewarded and monster is removed from the room.
        :return: None
        """
        room = self.player.current_room

        # if there are no monsters in the room
        if not room.monsters:
            self.ui.print("There is nothing here to fight.")
            return

        if monster_name not in room.monsters:
            self.ui.print("Invalid name.")
            return

        monster = room.monsters[monster_name]
        # one monster per fight for now
        self.ui.print(f"You engage the {monster.name}")
        self.ui.print(f"{monster.name} HP: {monster.hp}/{monster.max_hp}")
        self.ui.print(f"Your HP: {self.player.hp}/{self.player.max_hp}")

        # combat loop
        while self.player.is_alive() and monster.is_alive():
            self.ui.print("\nChoose your action:")
            self.ui.print("  1. Attack")
            self.ui.print("  2. Heal")
            self.ui.print("  3. Retreat")

            action = self.ui.get_key()
            m_hp = monster.hp
            attack = False
            self.ui.clear_logs()
            if action == "1":
                # player attacks first
                p_damage = self.player.attack(monster)
                # check if player has weapon
                if self.player.equipped_weapon is None:
                    self.ui.print(f"Warning! You have no weapon equipped.")
                    self.ui.print(f"You strike the {monster.name} with your fists for {p_damage}")
                else:
                    p_weapon = self.player.equipped_weapon.name
                    self.ui.print(f"You strike the {monster.name} with {p_weapon} for {p_damage}")
                attack=True
            elif action == "2":
                self.heal_player()

            elif action == "3":
                escape_chance = 0.6  # 60% success rate

                from random import random
                if random() < escape_chance:
                    self.ui.print("You successfully retreat from the fight!")
                    return  # exits combat, game continues

                else:
                    self.ui.print("Retreat failed! The monster strikes as you turn away!")
                    # monster gets a free hit
                    dmg = monster.attack(self.player)
                    self.ui.print(f"The {monster.name} hits you for {dmg} damage.")
                    self.ui.print(f"Your HP: {self.player.hp}/{self.player.max_hp}")

                    if not self.player.is_alive():
                        self.ui.print("You collapse while trying to escape...")
                        self.game_over = True
                        return

                    # continue to next round
                    continue
            else:
                self.ui.print("Invalid action.")
                continue

            if not monster.is_alive():
                break

            # monster attacks
            p_hp = self.player.hp
            m_damage = monster.attack(self.player)
            self.ui.print(f"The {monster.name} hits you for {m_damage} damage.")

            # show hp
            self.ui.print(f"Player HP: {p_hp} - {m_damage} --> {self.player.hp}/{self.player.max_hp}")
            if attack:
                self.ui.print(f"{monster.name} HP: {m_hp} - {p_damage} --> {monster.hp}/{monster.max_hp}")
            self.ui.draw_hud(self.player)

        # victory condition
        if monster.hp == 0:
            self.ui.print(f"{monster.name} has fallen.")

            # drop reward
            if monster.reward:
                self.ui.print(f"You have received: {monster.reward.name}\n")
                msg, picked_up = self.player.pick_up(monster.reward, self.ui)
                self.ui.print(msg)
                if not picked_up:
                    # add item to room
                    room.add_item(monster.reward)
                    self.ui.print(f"{monster.reward.name} has fallen to the floor.")


            # remove monster from room
            room.remove_monster(monster)

        # loss condition
        if self.player.hp == 0:
            self.ui.print("You have been defeated...")
            self.game_over = True



    def do_solve(self):
        """
            Allows player to attempt to solve the puzzle in the current room.
        :return: None
        """
        room = self.player.current_room
        if room.puzzle is None:
            self.ui.print("There is no puzzle here.")
            return

        message, reward = room.puzzle.attempt(self.ui)
        self.ui.print(message)

        if room.puzzle.solved:
            room.remove_puzzle()

        if reward:
            self.ui.print(f"You have received: {reward.name}")
            msg, picked_up = self.player.pick_up(reward, ui=self.ui)
            self.ui.print(msg)

            if not picked_up:
                # add item to room
                room.add_item(reward)
                self.ui.print(f"{reward.name} has fallen to the floor.")

    def show_player_storage(self):
        storage = self.player.storage
        player = self.player
        ui = self.ui
        if not storage:
            ui.print("Your storage is empty.")
            return

        selections = {}
        ui.print("[ STORAGE ]\n")

        for i, (name, item) in enumerate(storage.items(), start=1):
            ui.print(f"[{i}] {name} (W:{item.weight})")
            selections[str(i)] = item

        ui.print(f"\n[ CAP <{player.weight}/{player.max_weight}> ]")

        key = ui.get_key()
        if key in selections:
            self.inspect_item(selections[key])

    def inspect_item(self, item):
        ui = self.ui
        ui.clear_logs()

        ui.print(f"[ {item.name} ]")
        ui.print(f"{item.description}\n")

        actions = self.get_item_actions(item)

        for key, label, _ in actions:
            ui.print(f"[{key}] {label}")

        choice = ui.get_key()

        for key, _, action in actions:
            if choice == key:
                self.ui.clear_logs()
                msg = action()
                if msg:
                    ui.print(msg)
                return

    def get_item_actions(self, item):
        player = self.player
        actions = []

        # ---------------- WEAPONS ----------------
        if isinstance(item, Weapon):
            actions.append(("1", "Equip" if player.equipped_weapon != item else "Unequip",
                            lambda: self.ui.print(player.equip(item)) if player.equipped_weapon != item
                            else self.ui.print(player.unequip(item))))
            actions.append(("2", "Drop",
                            lambda: self.do_drop(item)))

        # ---------------- CONSUMABLES ----------------
        elif isinstance(item, Consumable):
            actions.append(("1", "Equip" if player.equipped_med != item else "Unequip",
                            lambda: self.ui.print(player.equip(item)) if player.equipped_med != item
                            else self.ui.print(player.unequip(item))))
            actions.append(("2", "Use", lambda: self.heal_player()))
            actions.append(("3", "Drop", lambda: self.do_drop(item)))

        # ---------------- MISC ----------------
        else:
            actions.append(("1", "Use", lambda: self.do_use(item)))
            actions.append(("2", "Drop", lambda: self.ui.print(player.remove_item(item))))

        return actions

    def print_help(self):
        """
        Prints a list of all available player commands.
        :return: None
        """
        self.ui.print("\nAvailable commands:\n")

        self.ui.print("Player:")
        self.ui.print("  [ARROW KEYS]       - Move to another room (north, south, east, west)")
        self.ui.print("  [I]                - View player's statistics")
        self.ui.print("  [S]                - View player's storage")
        self.ui.print("  [H]                - Heal player if healing item equipped")

        self.ui.print("\nItem Interaction:")
        self.ui.print("  [T]                - Pick up an item in the room")
        self.ui.print("  [S]                - Show items you're carrying")
        self.ui.print("  [R]                - List all entities in the room")

        self.ui.print("\nPuzzles:")
        self.ui.print("  [P]                - Attempt to solve the room's puzzle")

        self.ui.print("\nSystem:")
        self.ui.print("  [/]                - Show this help message")
        self.ui.print("  [Q]                - Exit the game\n")

def main():
    """Main entry point for the game."""
    while True:
        game = Game()
        result = game.run()

        if result == "quit":
            break

if __name__ == "__main__":
    main()
