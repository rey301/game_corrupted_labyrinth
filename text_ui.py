import curses


class TextUI:
    """A text-based user interface for the game using curses."""

    # Class constants
    ESC_DELAY_MS = 25
    SEPARATOR_LENGTH = 90
    HUD_HEIGHT = 1
    BOTTOM_MARGIN = 5  # Space reserved for logs and input

    def __init__(self):
        self.stdscr = None
        self.started = False

        # Layout tracking
        self.hud_y = None
        self.room_start_y = 1
        self.log_y = 0

    def start(self):
        """Initialize the curses screen and configure settings."""
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.set_escdelay(self.ESC_DELAY_MS)
        self.stdscr.keypad(True)
        self.started = True

    def stop(self):
        """Restore terminal to normal mode."""
        if not self.started:
            return

        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self):
        """Clear the entire screen."""
        self.stdscr.clear()
        self.stdscr.refresh()

    def get_screen_size(self):
        """Get current screen dimensions."""
        return self.stdscr.getmaxyx()

    def safe_addstr(self, y, x, text, max_width=None):
        """Safely add a string to the screen, handling curses errors."""
        h, w = self.get_screen_size()

        if y >= h or x >= w:
            return

        if max_width is None:
            max_width = w - 1

        try:
            self.stdscr.addstr(y, x, text[:max_width])
        except curses.error:
            pass

    def draw_separator(self, y):
        """Draw a horizontal separator line spanning the full terminal width."""
        h, w = self.get_screen_size()
        self.safe_addstr(y, 0, "-" * w)

    def draw_centered(self, text, y=None, clear=False):
        """
        Draw text centered horizontally on the screen.

        Args:
            text: String or multi-line string to center
            y: Starting y position (None = current position)
            clear: Whether to clear screen first

        Returns:
            The y position after the last line drawn
        """
        if clear:
            self.stdscr.clear()

        h, w = self.get_screen_size()
        lines = str(text).split("\n")

        if y is None:
            y, _ = self.stdscr.getyx()

        for i, line in enumerate(lines):
            current_y = y + i
            if current_y >= h:
                break

            # Calculate centered x position
            line_length = len(line)
            x = max(0, (w - line_length) // 2)

            self.safe_addstr(current_y, x, line, w - x)

        self.stdscr.refresh()
        return y + len(lines)

    def draw_room(self, room_desc):
        """Draw the room description centered with full-width separators."""
        self.stdscr.clear()
        h, w = self.get_screen_size()

        y = 0

        # Top separator
        self.draw_separator(y)
        y += 1

        # Room description - centered
        lines = room_desc.strip("\n").split("\n")
        for line in lines:
            if y >= h - self.BOTTOM_MARGIN:
                break

            # Calculate centered x position
            line_length = len(line)
            x = max(0, (w - line_length) // 2)
            self.safe_addstr(y, x, line, w - x)
            y += 1

        # Bottom separator before HUD
        if y < h - self.BOTTOM_MARGIN:
            self.draw_separator(y)
            y += 1

        # Reserve space for HUD
        self.hud_y = y
        y += self.HUD_HEIGHT

        # Separator after HUD
        if y < h - self.BOTTOM_MARGIN:
            self.draw_separator(y)
            y += 1

        # Set log starting position
        self.room_start_y = y
        self.log_y = y

        self.stdscr.refresh()

    def draw_hud(self, player):
        """Draw the heads-up display with player stats."""
        h, w = self.get_screen_size()

        # Build HUD components
        hp = f"HP: {player.hp}/{player.max_hp}"
        atk = f"ATK: {player.attack_power}"
        wpn = f"WPN: {player.equipped_weapon.name if player.equipped_weapon else 'Fists'}"

        med = "MED: --"
        if player.equipped_med:
            med = f"MED: {player.equipped_med.name} [{player.equipped_med.uses}/{player.equipped_med.max_uses}]"

        cap = f"CAP: {player.weight}/{player.max_weight}"

        hud_text = f"{hp}   {med}   {cap}   {atk}   {wpn}"

        # Clear and redraw HUD line
        self.stdscr.move(self.hud_y, 0)
        self.stdscr.clrtoeol()
        self.safe_addstr(self.hud_y, 0, hud_text, w - 1)

        self.stdscr.refresh()

    def print(self, text):
        """Print text to the log area, with automatic overflow handling."""
        h, w = self.get_screen_size()
        lines = str(text).split("\n")

        for line in lines:
            if self.log_y >= h - 1:
                self.clear_logs()
                break

            self.safe_addstr(self.log_y, 0, line, w - 1)
            self.log_y += 1

        self.stdscr.refresh()

    def clear_logs(self):
        """Clear the log area below the HUD."""
        h, w = self.get_screen_size()

        for y in range(self.room_start_y, h - 1):
            try:
                self.stdscr.move(y, 0)
                self.stdscr.clrtoeol()
            except curses.error:
                pass

        self.log_y = self.room_start_y
        self.stdscr.refresh()

    def get_key(self):
        """Get a single key press from the user."""
        key = self.stdscr.getch()

        if key == 27:  # ESC key
            return "ESC"

        if 0 <= key <= 255:
            return chr(key)

        return key

    def get_text(self, prompt="> "):
        """Get a line of text input from the user."""
        self.print(prompt)

        curses.echo()
        y, x = self.stdscr.getyx()
        text = self.stdscr.getstr(y, x).decode("utf-8")
        curses.noecho()

        return text

    def redraw_game(self, room, player):
        """Redraw the entire game screen."""
        self.clear()
        self.draw_room(room.description)
        self.draw_hud(player)

    # Legacy methods (kept for compatibility)
    def input(self, prompt=""):
        """Legacy method - reads input using built-in input()."""
        return input(prompt)

    def draw_top(self, text, y=0, clear=True):
        """Legacy method - draw text at the top of the screen."""
        if clear:
            self.stdscr.clear()

        h, w = self.get_screen_size()
        lines = str(text).split("\n")

        for i, line in enumerate(lines):
            if y + i >= h:
                break
            self.safe_addstr(y + i, 0, line, w - 1)

        self.stdscr.refresh()

    def get_inp(self, prompt="> "):
        """Legacy method - alias for get_text()."""
        return self.get_text(prompt)