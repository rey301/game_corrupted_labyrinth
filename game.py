from player import Player
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

        self.player = Player("Lapel","",5, 5, 1)
        self.ui = TextUI()
        self.parser = Parser(self.ui)
        self.world = WorldBuilder()
        self.game_over = False

    def play(self):
        """
            The main play loop that displays welcome message, reads player input
            in a loop, processes commands, and terminates when game_over becomes
            True.
        :return: None
        """
        # initialise world and intro messages
        start_room = self.world.build()
        self.player.set_current_room(start_room)
        self.ui.print("Welcome to the Labyrinth. \nType HELP to see available commands.\n")
        self.ui.print(self.player.current_room.describe())

        # main game loop
        while not self.game_over and self.player.is_alive():
            command = self.parser.get_command()
            self.game_over = self.process(command)
        print("Thank you for playing!")


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

    def do_go(self, direction):
        """
        Move player into room given the direction, and if exit doesn't exist;
        error message is displayed.
        :param direction: Direction the player wishes to move (e.g. north, east)
        """
        if direction is None:
            self.ui.print("Go where?")
            return
        next_room = self.player.current_room.get_exit(direction)

        if next_room is not None:
            self.player.current_room = next_room
            self.ui.print(self.player.current_room.describe())

    def do_scan(self, obj):
        """
        Inspect an object which could be an item, a monster, a puzzle, or the whole room.
        :param obj: This is the object that the user defines (e.g. item name)
        :return: None
        """
        room = self.player.current_room
        if obj is None:
            self.ui.print("Scan what?")
            return

        # inspecting an item in the room
        if obj in room.items:
            item = room.items[obj]
            lines = [item.description]

            if isinstance(item, Weapon):
                lines.append(f" | ATTACK POWER {item.damage}")

            if isinstance(item, Consumable):
                lines.append(f" | HEALING {item.heal}")

            if isinstance(item, Misc):
                lines.append(f" | DATA SIGNATURE: {item.misc_id}")
            self.ui.print("".join(lines))

            return

        # inspecting item in storage
        if obj in self.player.storage:
            item = self.player.storage[obj]
            self.ui.print(f"{item.description}")
            if isinstance(item, Weapon):
                self.ui.print(f"ATTACK POWER {item.damage}")
            return

        # inspecting a monster
        if obj in room.monsters:
            monster = room.monsters[obj]
            self.ui.print(f"{monster.description}")
            self.ui.print(f"ATTACK POWER {monster.attack_power}")
            return

        # inspect the room for everything
        if obj == "room":
            room = self.player.current_room

            # If the room contains nothing of interest
            if not room.items and not room.monsters and not room.puzzle:
                self.ui.print("The room reveals nothing unusual.")
                return

            lines = ["=== SCANNING ROOM ===\n"]

            # ITEMS ---------------------------------------------------------
            if room.items:
                lines.append("[ Items Detected ]")
                for item_name, item in room.items.items():
                    lines.append(f" - {item_name}")
                lines.append("")  # blank line
            else:
                lines.append("[ No Items Detected ]\n")

            # MONSTERS ------------------------------------------------------
            if room.monsters:
                lines.append("[ Hostile Entities ]")
                for monster in room.monsters:
                    lines.append(f" • {room.monsters[monster].name}")
                lines.append("")
            else:
                lines.append("[ No Hostiles Present ]\n")

            # PUZZLE --------------------------------------------------------
            if room.puzzle:
                lines.append("[ Corrupted Engram Detected ]")
                lines.append(f" • Puzzle: {room.puzzle.name}\n")

            lines.append("=== END OF ROOM SCAN ===")

            self.ui.print("\n".join(lines))
            return

            return

        self.ui.print("Invalid string name, try again.")

    def do_take(self, item_name):
        """
        Attempt to pick up an item from the current room and put it in the
        player's backpack.
        :param item_name: Name of the item the player wishes to pick up.
        :return: None
        """
        room = self.player.current_room
        if item_name is None:
            self.ui.print("Take what?")
            return
        if item_name not in room.items:
            self.ui.print("That item is not here.")
            return

        item = room.items[item_name]
        prev_weight = self.player.weight
        success = self.player.pick_up(item)
        if success:
            self.ui.print(f"{item_name} added to storage.")
            self.ui.print(f"Storage: {prev_weight} + {item.weight} --> {self.player.weight}/{self.player.max_weight} bytes")
            self.player.current_room.remove_item(item)
        else:
            self.ui.print(f"{item.name} is too heavy to carry.")

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
                healed = item.use(self.player)
                self.ui.print(f"You use {item.name}. {healed}")
                self.player.storage.pop(item_name)
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
        monster = room.monsters[monster_name]

        # if there are no monsters in the room
        if not room.monsters:
            self.ui.print("There is nothing here to fight.")
            return

        # one monster per fight for now
        self.ui.print(f"You engage the {monster.name}")

        # combat loop
        while self.player.is_alive() and monster.is_alive():
            # player attacks first
            m_hp = monster.hp
            p_damage = self.player.attack(monster)
            # check if player has weapon
            if self.player.equipped_weapon is None:
                self.ui.print(f"You strike the {monster.name} with your fists for {p_damage}")
            else:
                p_weapon = self.player.equipped_weapon.name
                self.ui.print(f"You strike the {monster.name} with {p_weapon} for {p_damage}")

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
                room.add_item(monster.reward)
                self.ui.print(f"The {monster.name} dropped: {monster.reward.name}")

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

        result = room.puzzle.attempt(self.ui)
        self.ui.print(result)

        if room.puzzle.solved and room.puzzle.reward:
            self.retrieve_puzzle_reward(room.puzzle.reward, room)

    def retrieve_puzzle_reward(self, reward, room):
        if reward == "unlock_hidden_packet":
            self.ui.print("A corrupted packet materialises on the floor...")

            phantom_key = Misc(
                "phantom_key",
                "A strange block of corrupted data. It seems to resonate with unseen doorways.",
                weight=1,
                misc_id="unlock_c0"
            )
            room.add_item(phantom_key)

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
    game.play()

if __name__ == "__main__":
    main()
