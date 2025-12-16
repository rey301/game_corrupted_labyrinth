class Menu:
    def __init__(self, ui, game):
        self.ui = ui
        self.game = game

    def pause(self):
        self.game.pause = True
        self.ui.draw_top(
            "=== SYSTEM PAUSED ===\n\n"
            "[ESC] Resume\n"
            "[R] Restart\n"
            "[Q] Quit"
        )
        while True:
            key = self.ui.get_key()
            if key == "ESC":
                self.ui.redraw_game(
                    self.game.player.current_room,
                    self.game.player
                )
                self.game.pause = False
                return None
            if key == "r":
                self.ui.clear()
                return "restart"
            if key == "q":
                return "quit"

    def game_over(self):
        """Display game over menu and handle selection."""
        text = (
            "=== SYSTEM FAILURE ===\n"
            "You have been terminated.\n\n"
            "[R] Restart\n"
            "[Q] Quit"
        )
        self.ui.draw_top(text)

        while True:
            key = self.ui.get_key()
            if key == "r":
                self.ui.clear()
                return "restart"
            elif key == "q":
                return "quit"