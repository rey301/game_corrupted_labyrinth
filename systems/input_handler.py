import curses

class InputHandler:
    """
    This class handles input from the use the executes certain methods given a Game object.
    """
    def __init__(self, game):
        self.game = game

        self.movement = {
            curses.KEY_UP: "north",
            curses.KEY_DOWN: "south",
            curses.KEY_LEFT: "west",
            curses.KEY_RIGHT: "east",
        }

        self.actions = {
            "r": game.scan_room,
            "p": lambda: game.solver.do_solve(),
            "t": game.display_items,
            "h": game.heal_player,
            "s": lambda: game.inventory.show_player_storage(),
            "i": lambda: game.ui.display_text(game.player.show_stats()),
            "/": game.ui.print_help,
        }

    def handle(self, key):
        """
        When a certain key is given (pressed) then an action is executed depending on the key
        (movement is handled by another class). If no key or space is pressed then nothing happens, but any other key
        will display a help message to the user.
        :param key: The key that is pressed by the user.
        :return: None
        """
        if key == -1 or key == " ":
            return
        else:
            self.game.ui.clear_logs()
            if key == "ESC":
                self.game.pause = True
                return

            if key in self.movement:
                self.game.move(self.movement[key])
                return

            if key in self.actions:
                self.actions[key]()
                return

            self.game.ui.display_text("Unknown command.\nPress '/' for available commands.")

