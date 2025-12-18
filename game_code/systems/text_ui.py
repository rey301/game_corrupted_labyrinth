import curses
import time


class TextUI:
    """
    A text-based user interface built using the curses library.
    It renders rooms, HUD, logs, and menus, handling keyboard input, managing screen layout and typing animation.
    """

    # class constants
    ESC_DELAY_MS = 25 # so that the user can press escape only once
    HUD_HEIGHT = 1
    BOTTOM_MARGIN = 5  # space reserved for logs and input
    TYPING_SPEED = 0.03 # seconds per character

    def __init__(self):
        self.screen = None
        self.started = False

        # layout tracking
        self.hud_y = None
        self.room_start_y = 1
        self.log_y = 0
        self.log_x = 0

        # typing animation toggle
        self.typing_enabled = True

    def start_screen(self):
        """
        Initialise the curses screen and configure terminal settings.

        Must be called before any rendering happens as it switches the terminal into curses mode and enables
        non-blocking keyboard input.
        :return: None
        """
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        # for windows
        if hasattr(curses, "set_escdelay"):
            curses.set_escdelay(self.ESC_DELAY_MS)

        self.screen.keypad(True)
        self.screen.nodelay(True)  # Make getch() non-blocking
        self.started = True

    def stop_screen(self):
        """
        Restore terminal to normal mode, and is only called when the game exits to prevent terminal corruption.
        """
        if not self.started:
            return

        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self):
        """
        Clear the entire screen.
        """
        self.screen.clear()
        self.screen.refresh()

    def get_screen_size(self):
        """
        Get current screen dimensions.
        """
        return self.screen.getmaxyx()

    def safe_draw(self, y, x, text, max_width=None):
        """
        Safely draw text to the screen given a position; this prevents crashes caused by drawing outside
        the screen bounds or curses rendering errors.
        :param y: Vertical screen position
        :param x: Horizontal screen position
        :param text: Text to render
        :param max_width: Max width to draw text
        :return:
        """
        h, w = self.get_screen_size()

        # check if position is larger than the screen
        if y >= h or x >= w:
            return

        if max_width is None:
            max_width = w - 1

        try:
            self.screen.addstr(y, x, text[:max_width])
        except curses.error:
            pass

    def draw_separator(self, y):
        """
        Draw a horizontal separator line spanning the full terminal width.
        """
        h, w = self.get_screen_size()
        self.safe_draw(y, 0, "-" * w)

    def draw_centered(self, text, y=None, clear=False):
        """
        Draw text centered horizontally on the screen.
        :param text: String or multi-line string to center
        :param y: Starting y position (None means the starting position)
        :param clear: Whether to clear screen first
        :return: The y position after the last line drawn
        """
        if clear:
            self.screen.clear()

        h, w = self.get_screen_size()
        lines = str(text).split("\n")

        if y is None:
            y, _ = self.screen.getyx()

        for i, line in enumerate(lines):
            current_y = y + i
            if current_y >= h:
                break

            # calculate centered x position
            line_length = len(line)
            x = max(0, (w - line_length) // 2)

            self.safe_draw(current_y, x, line, w - x)

        self.screen.refresh()
        return y + len(lines)

    def draw_room(self, room_desc):
        """
        Draw the room description centered with full-width separators, where space is reserved for the HUD and
        log output.
        :param room_desc: The description of the room
        :return: None
        """
        self.screen.clear()
        h, w = self.get_screen_size()

        y = 0

        # top separator
        self.draw_separator(y)
        y += 1

        # center the room description
        lines = room_desc.strip("\n").split("\n")
        for line in lines:
            if y >= h - self.BOTTOM_MARGIN:
                break

            # calculate centered x position
            line_length = len(line)
            x = max(0, (w - line_length) // 2)
            self.safe_draw(y, x, line, w - x)
            y += 1

        # bottom separator before hud
        if y < h - self.BOTTOM_MARGIN:
            self.draw_separator(y)
            y += 1

        # reserve space for hud
        self.hud_y = y
        y += self.HUD_HEIGHT

        # separator after hud
        if y < h - self.BOTTOM_MARGIN:
            self.draw_separator(y)
            y += 1

        # set log starting position
        self.room_start_y = y
        self.log_y = y

        self.screen.refresh()

    def draw_hud(self, player):
        """
        Draw the heads-up display with player stats, centered.
        :param player: The player in which the stats are pulled from.
        :return: None
        """
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

        # clear hud line
        self.screen.move(self.hud_y, 0)
        self.screen.clrtoeol()

        # calculate centered x position and draw hud
        hud_length = len(hud_text)
        x = max(0, (w - hud_length) // 2)
        self.safe_draw(self.hud_y, x, hud_text, w - x)

        self.screen.refresh()

    def display_text(self, text, typing=None, end="\n"):
        """
        Display text in the log area with optional typing animation, which can be skipped using the space bar.
        It can print multiline text and use inline printing (two print statements on one line).
        :param text: The text to display.
        :param typing: Allows typing animation to be set.
        :param end: Line ending character where the default is a newline.
        :return: None
        """
        h, w = self.get_screen_size()

        lines = str(text).split("\n")

        use_typing = self.typing_enabled if typing is None else typing

        for line_idx, line in enumerate(lines):
            # clear logs if we hit the bottom
            if self.log_y >= h - 1:
                self.clear_logs()
                self.log_y = 0
                self.log_x = 0
                break

            # calculate available width on current line
            # if starting a new line, log_x is 0 but if appending, > 0
            available_w = w - self.log_x

            if use_typing:
                skipped = False
                # offset the characters index by the current log_x position
                for i, char in enumerate(line):
                    if i >= available_w - 1:
                        break

                    # Print at log_y, log_x + i
                    self.safe_draw(self.log_y, self.log_x + i, char)
                    self.screen.refresh()

                    if self.get_key() == " ":
                        remaining = line[i + 1:available_w - 1]
                        if remaining:
                            self.safe_draw(self.log_y, self.log_x + i + 1, remaining)
                            self.screen.refresh()
                        skipped = True
                        break

                    time.sleep(self.TYPING_SPEED)

                if skipped:
                    use_typing = False
            else:
                # print entire line at starting position log_x using safe_draw
                self.safe_draw(self.log_y, self.log_x, line, w - 1)

            # update log_x based on the length of text
            self.log_x += len(line)

            # handling newlines
            if line_idx < len(lines) - 1:
                self.log_y += 1
                self.log_x = 0

            # if this is the last part, check the end parameter
            elif line_idx == len(lines) - 1:
                if end == "\n":
                    self.log_y += 1
                    self.log_x = 0
                else:
                    # if not a newline, we stay on this line.
                    if end:
                        self.safe_draw(self.log_y, self.log_x, end)
                        self.log_x += len(end)

        self.screen.refresh()

    def wait_to_start_game(self, prompt="Press SPACE to begin initialisation..."):
        """
        Used to display a prompt to the user after welcome message is shown, to allow the player to start the game.
        :param prompt: The prompt in which is displayed.
        :return: None
        """
        self.display_text(f"\n{prompt}", typing=False)

        # set blocking mode temporarily
        self.screen.nodelay(False)
        self.screen.getch()
        self.screen.nodelay(True)

    def set_typing_speed(self, speed):
        """
        Set the typing animation speed.
        :param speed: Seconds per characters (e.g., 0.05 for slower, 0.01 for faster).
        :return: None
        """
        self.TYPING_SPEED = speed

    def toggle_typing(self, enabled=None):
        """
        Enable or disable typing animation.
        :param enabled: True to enable, False to disable, None to toggle.
        :return: None
        """
        if enabled is None:
            self.typing_enabled = not self.typing_enabled
        else:
            self.typing_enabled = enabled

    def clear_logs(self):
        """
        Clear the log area below the HUD.
        :return: None
        """
        h, w = self.get_screen_size()

        for y in range(self.room_start_y, h - 1):
            try:
                self.screen.move(y, 0)
                self.screen.clrtoeol()
            except curses.error:
                pass

        self.log_y = self.room_start_y
        self.screen.refresh()

    def get_key(self):
        """
        Get a single key press from the user.
        :return: A string "ESC" if the user pressed ESC key or the character string for any key.
        """
        key = self.screen.getch()

        if key == 27:  # ESC key
            return "ESC"

        if 0 <= key <= 255:
            return chr(key)

        return key

    def wait_for_key(self):
        """
        This loops until a key is pressed.
        :return: The key if a key is pressed.
        """
        while True:
            key = self.get_key()
            if key != -1 and key != " ":
                return key

    def redraw_game(self, room, player):
        """
        Redraw the entire game screen.
        :param room: The room in which the description is used to display.
        :param player: Used so that the player's stats can be displayed on the HUD.
        :return: None
        """
        self.clear()
        self.draw_room(room.description)
        self.draw_hud(player)

    def draw_top(self, text, y=0, clear=True):
        """
        Draw text at the top of the screen.
        :param text: The text to be drawn.
        :param y: Defaulted at 0, which is the left most side.
        :param clear: Defaulted to True, which clears the whole screen.
        :return: None
        """
        if clear:
            self.screen.clear()

        h, w = self.get_screen_size()
        lines = str(text).split("\n")

        for i, line in enumerate(lines):
            if y + i >= h:
                break
            self.safe_draw(y + i, 0, line, w - 1)

        self.screen.refresh()

    def get_text(self, prompt="> "):
        """
        Get a line of text input from the user.

        This switches out of blocking mode with a visible cursor and echo enabled.
        :param prompt: The input prompt displayed to the user.
        :return: The user text that is inputted.
        """
        self.display_text(prompt)

        # typing mode
        curses.echo()  # show typed characters
        curses.curs_set(1)  # show the blinking cursor
        self.screen.nodelay(False)  # force the program to wait for input

        # get current cursor position to type right after the prompt
        y, x = self.screen.getyx()

        # get input
        try:
            # getstr returns bytes, so we decode to string
            input_bytes = self.screen.getstr(y, x)
            text = input_bytes.decode("utf-8")
        except Exception:
            text = ""

        # restore back to non-blocking mode
        self.screen.nodelay(True)
        curses.curs_set(0)  # hide cursor
        curses.noecho()  # doesn't echo characters

        return text

    def print_welcome(self):
        """
        Prints the welcome text for the game.
        :return: None
        """
        self.display_text("""> INITIALISING SESSION...
> LOADING USER MEMORY.............
> CHECKSUM ERROR IN SECTOR 0

[ WARNING ]
Your consciousness has been loaded into an unstable system.

Fragments of memory are missing.
Paths are corrupted.
Something hostile is running in the background.

You don't remember how you got here.
You don't remember who you were.

You only know one thing:
YOU MUST REACH THE KERNEL
AND ESCAPE BEFORE THE SYSTEM COLLAPSES
        """)

    def print_help(self):
        """
        Display all available commands.
        :return: None
        """
        self.display_text("""COMMANDS:
Player:
  [ARROW KEYS]       - Move to another room
  [I]                - View player's statistics
  [S]                - View player's storage
  [H]                - Heal player if healing item equipped

Item Interaction:
  [T]                - Pick up an item in the room
  [R]                - Scan all entities in the room

Puzzles:
  [P]                - Attempt to solve the room's puzzle

System:
  [/]                - Show this help message
  [ESC]              - Pause menu""",
                          False)