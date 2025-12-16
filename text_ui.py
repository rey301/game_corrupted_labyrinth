import curses
import time


class TextUI:
    """A text-based user interface for the game using curses."""

    # Class constants
    ESC_DELAY_MS = 25
    SEPARATOR_LENGTH = 90
    HUD_HEIGHT = 1
    BOTTOM_MARGIN = 5  # Space reserved for logs and input
    TYPING_SPEED = 0.03 # Seconds per character (adjustable)

    def __init__(self):
        self.stdscr = None
        self.started = False

        # Layout tracking
        self.hud_y = None
        self.room_start_y = 1
        self.log_y = 0

        # Typing animation toggle
        self.typing_enabled = True

    def start(self):
        """Initialize the curses screen and configure settings."""
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.set_escdelay(self.ESC_DELAY_MS)
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)  # Make getch() non-blocking
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
        """Draw the heads-up display with player stats, centered."""
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

        # Clear HUD line
        self.stdscr.move(self.hud_y, 0)
        self.stdscr.clrtoeol()

        # Calculate centered x position and draw HUD
        hud_length = len(hud_text)
        x = max(0, (w - hud_length) // 2)
        self.safe_addstr(self.hud_y, x, hud_text, w - x)

        self.stdscr.refresh()

    def print(self, text, typing=None):
        """
        Print text to the log area with optional typing animation.
        User can press any key to skip the animation.

        Args:
            text: Text to print
            typing: Override typing animation (True/False/None for default)
        """
        h, w = self.get_screen_size()
        lines = str(text).split("\n")

        # Determine if typing animation should be used
        use_typing = self.typing_enabled if typing is None else typing

        for line in lines:
            if self.log_y >= h - 1:
                self.clear_logs()
                break

            if use_typing:
                # Type out character by character with skip detection
                skipped = False
                for i, char in enumerate(line):
                    if i >= w - 1:
                        break

                    self.safe_addstr(self.log_y, i, char)
                    self.stdscr.refresh()

                    # Check if user pressed a key to skip
                    if self.get_key() == " ":
                        # Print the rest of the line instantly
                        remaining = line[i + 1:w - 1]
                        if remaining:
                            self.safe_addstr(self.log_y, i + 1, remaining)
                            self.stdscr.refresh()
                        skipped = True
                        break

                    time.sleep(self.TYPING_SPEED)

                # If animation was skipped, disable typing for remaining lines
                if skipped:
                    use_typing = False
            else:
                # Print entire line at once
                self.safe_addstr(self.log_y, 0, line, w - 1)

            self.log_y += 1

        self.stdscr.refresh()

    def _check_skip_input(self):
        """Check if user pressed any key (non-blocking)."""
        try:
            key = self.stdscr.getch()
            if key != -1:  # -1 means no key was pressed
                return True
        except:
            pass
        return False

    def wait_for_key(self, prompt="Press any key to continue..."):
        """
        Display a message and wait for user to press any key.

        Args:
            prompt: Message to display
        """
        self.print(f"\n{prompt}", typing=False)

        # Set blocking mode temporarily
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)

    def set_typing_speed(self, speed):
        """
        Set the typing animation speed.

        Args:
            speed: Seconds per character (e.g., 0.05 for slower, 0.01 for faster)
        """
        self.TYPING_SPEED = speed

    def toggle_typing(self, enabled=None):
        """
        Enable or disable typing animation.

        Args:
            enabled: True to enable, False to disable, None to toggle
        """
        if enabled is None:
            self.typing_enabled = not self.typing_enabled
        else:
            self.typing_enabled = enabled

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

        # --- ENTER TYPING MODE ---
        curses.echo()  # Show typed characters
        curses.curs_set(1)  # Show the blinking cursor
        self.stdscr.nodelay(False)  # Force the program to WAIT for input

        # Get current cursor position to type right after the prompt
        y, x = self.stdscr.getyx()

        # Capture the input
        try:
            # getstr returns bytes, so we decode to string
            input_bytes = self.stdscr.getstr(y, x)
            text = input_bytes.decode("utf-8")
        except Exception:
            text = ""

        # --- RESTORE GAME MODE ---
        self.stdscr.nodelay(True)  # Return to non-blocking mode (game loop)
        curses.curs_set(0)  # Hide the cursor again
        curses.noecho()  # Stop echoing characters

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