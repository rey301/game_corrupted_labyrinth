from player import Player
import curses
from parser import Parser
from world_builder import WorldBuilder
from text_ui import TextUI
from weapon import Weapon
from consumable import Consumable
from misc import Misc

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
        try:
            self.ui.start()
            self.play()
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
        self.ui.print("Welcome to the Labyrinth. \nType HELP to see available commands.\n")
        self.ui.draw_room(self.player.current_room.describe())
        self.ui.draw_hud(self.player)

        # main game loop
        while not self.game_over and self.player.is_alive():
            key = self.ui.get_key()
            self.handle_key(key)


    def handle_key(self, key):
        if key == curses.KEY_UP:
            self.move("north")
        elif key == curses.KEY_DOWN:
            self.move("south")
        elif key == curses.KEY_LEFT:
            self.move("west")
        elif key == curses.KEY_RIGHT:
            self.move("east")

        elif key == "s":
            self.scan_room()

        elif key == 'e':
            self.take_item()

        elif key == 'e':
            self.equip_weapon()

        elif key == 'f':
            self.fight()

        elif key == 'p':
            self.solve_puzzle()

        elif key == 'l':
            self.look()

        elif key == 'i':
            self.ui.print(self.player.show_storage())

        elif key == 'c':
            self.ui.print(self.player.show_stats())

        elif key == 'h':
            self.print_help()

        elif key == 'q':
            self.game_over = True

        self.ui.draw_hud(self.player)


    def process(self, command):
        """
            Handles user commands and invokes an action method from
            the command given (e.g. item interaction, problem solving).
        :param command: Parse command object containing the verb and obj (optional)
        :return: True if game should end (quit or player dies), otherwise False if game continues
        """

        verb = command.verb
        obj = command.obj

        # unknown command
        if verb is None:
            self.ui.print("I don't understand that command.")
            return False

        # movement
        if verb == "go":
            self.do_go(obj)
            return False

        elif verb == "look":
            self.ui.print(self.player.current_room.describe())
            return False

        elif verb == "stats":
            self.ui.print(self.player.show_stats())
            return False

        # looking for items in the room
        elif verb == "scan":
            self.do_scan(obj)
            return False

        # show storage
        elif verb == "storage":
            self.ui.print(self.player.show_storage())
            return False

        # take item
        elif verb == "take":
            self.do_take(obj)
            return False

        # drop item
        elif verb == "drop":
            self.do_drop(obj)
            return False

        # use item
        elif verb == "use":
            self.do_use(obj)
            return False

        # equip a weapon
        elif verb == "equip":
            self.do_equip(obj)
            return False

        # fight monster
        elif verb == "fight":
            self.do_fight(obj)
            return False

        # solve puzzle
        elif verb == "solve":
            self.do_solve()
            return False

        # help menu
        elif verb == "help":
            self.print_help()
            return False

        # quit game
        elif verb == "quit":
            return True  # This ends the game loop

        # otherwise
        else:
            self.ui.print("That command is not implemented.")
            return False

    def move(self, direction):
        """
        Move player into room given the direction, and if exit doesn't exist;
        error message is displayed.
        :param direction: Direction the player wishes to move (e.g. north, east)
        """
        room = self.player.current_room

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
                # ask user if they want to unlock it
                answer = self.ui.input(f"Use {key_item.name} to unlock? (yes/no)\n> ").strip().lower()

                # unlock the door
                if answer in ("yes", "y"):
                    self.do_use(key_item.name) # use the item
                    self.ui.print(f"You enter the {next_room.name}")
                    self.player.current_room = next_room
                    self.ui.print(self.player.current_room.describe())
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
        self.ui.clear_logs()

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
        self.ui.clear_logs()
        item_count = 1
        selections = {}

        if not bool(room.items):
            self.ui.print("There are no items to pick up.")
            return
        else:
            self.ui.print("Pick an item:\n")
            for item_name in room.items:
                self.ui.print(f"[{str(item_count)}] {item_name}")
                selections[str(item_count)] = room.items[item_name]
                item_count += 1

            key = self.ui.get_key()
            chosen_item = selections[key]
            msg, flag = self.player.pick_up(room.items[chosen_item.name], self.ui)
            self.ui.clear_logs()
            self.ui.print(msg)
            return

    def do_drop(self, item_name):
        """
        Select an item to drop from player's storage and is place in the room.
        :param item_name: The item the player wishes to drop.
        :return: None
        """
        room = self.player.current_room

        if item_name is None:
            self.ui.print("Drop what?")
            return

        if item_name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        # remove from storage
        item = self.player.storage[item_name]
        self.ui.print(self.player.remove_item(item_name))

        # add item to room
        room.add_item(item)

        self.ui.print(f"{item_name} has fallen to the floor.")

    def do_use(self, item_name):
        """
        Allows player to use an item from their backpack, applying whatever
        effect the item has.
        :param item_name: Name of the item to use.
        :return: None
        """
        if item_name is None:
            self.ui.print("Use what?")
            return

        if item_name not in self.player.storage:
            self.ui.print("You don't have that item.")
            return

        item = self.player.storage[item_name]

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
                    self.ui.print(self.player.remove_item(item.name))
            else:
                self.ui.print(f"You can't use {item.name} here.")
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
            self.ui.clear_logs()
            if action == "1":
                # player attacks first
                m_hp = monster.hp
                p_damage = self.player.attack(monster)
                # check if player has weapon
                if self.player.equipped_weapon is None:
                    self.ui.print(f"Warning! You have no weapon equipped.")
                    self.ui.print(f"You strike the {monster.name} with your fists for {p_damage}")
                else:
                    p_weapon = self.player.equipped_weapon.name
                    self.ui.print(f"You strike the {monster.name} with {p_weapon} for {p_damage}")
            elif action == "2" or action.lower() == "heal":
                consumables = self.player.get_consumables()

                if not consumables:
                    self.ui.print("You have no healing items!")
                    continue

                self.ui.print("Choose a healing item:")
                for name, item in consumables.items():
                    self.ui.print(f" - {name} (+{item.heal} HP")

                heal_choice = self.ui.input("> ").strip()

                if heal_choice in consumables:
                    item = consumables[heal_choice]
                    message = item.use(self.player)
                    self.ui.print(message)
                    self.player.remove_item(item.name)
                else:
                    self.ui.print("Invalid healing item.")
                    continue
            elif action == "3" or action.lower() == "retreat":
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
            self.ui.print(f"{monster.name} HP: {m_hp} - {p_damage} --> {monster.hp}/{monster.max_hp}")

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

    def print_help(self):
        """
        Prints a list of all available player commands.
        :return: None
        """
        self.ui.print("\nAvailable commands:\n")

        self.ui.print("Player:")
        self.ui.print("  go <direction>     - Move to another room (north, south, east, west)")
        self.ui.print("  look               - Reprint the current room's description")
        self.ui.print("  stats              - View player's statistics")

        self.ui.print("\nItem Interaction:")
        self.ui.print("  take <item>        - Pick up an item in the room")
        self.ui.print("  use <item>         - Use a misc or consumable item")
        self.ui.print("  equip <weapon>     - Equip a weapon from your backpack")
        self.ui.print("  storage            - Show items you're carrying")
        self.ui.print("  scan room          - List all entities in the room")
        self.ui.print("  scan <entity>      - Examine an entity in the room or in your storage")

        self.ui.print("\nCombat:")
        self.ui.print("  fight              - Engage in combat with the monster here")

        self.ui.print("\nPuzzles:")
        self.ui.print("  solve              - Attempt to solve the room's puzzle")

        self.ui.print("\nSystem:")
        self.ui.print("  help               - Show this help message")
        self.ui.print("  quit               - Exit the game\n")

def main():
    """Main entry point for the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
