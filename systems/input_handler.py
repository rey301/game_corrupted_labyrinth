import curses

class InputHandler:
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
            "t": game.take_item,
            "h": game.heal_player,
            "s": lambda: game.inventory.show_player_storage(),
            "i": lambda: game.ui.print(game.player.show_stats()),
            "/": game.print_help,
        }

    def handle(self, key):
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

            self.game.ui.print("Unknown command.\nPress '/' for available commands.")