import curses

class TextUI:
    """A simple text based User Interface (UI) for the game."""
    def __init__(self):
        self.stdscr = None
        self.started = False
        self.room_height = 14
        self.log_y = 0

    def input(self, prompt=""):
        """
            Reads a line of text entered by the user.
        :return:
        """
        return input(prompt)

    def start(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.started = True

    def stop(self):
        if not self.started:
            return
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def clear(self):
        self.stdscr.clear()
        self.stdscr.refresh()

    def print(self, text):
        h, w = self.stdscr.getmaxyx()
        lines = str(text).split("\n")

        for line in lines:
            if self.log_y >= h - 1:
                break  # stop before overflow
            try:
                self.stdscr.addstr(self.log_y, 0, line[:w - 1])
            except curses.error:
                pass
            self.log_y += 1

        self.stdscr.refresh()

    def get_key(self):
        key = self.stdscr.getch()
        if 0 <= key <= 255:
            return chr(key)
        self.stdscr.refresh()
        return key

    def get_text(self, prompt="> "):
        curses.echo()
        self.print(prompt)
        y, x = self.stdscr.getyx()
        text = self.stdscr.getstr(y, x).decode("utf-8")
        curses.noecho()
        return text

    def draw_room(self, room_desc):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        y = 0
        lines = room_desc.strip("\n").split("\n")

        line_len = 90
        # separator line
        if y == 0:
            try:
                self.stdscr.addstr(y, 0, "-" * line_len)
            except curses.error:
                pass
            y += 1

        for line in lines:
            if y >= h - 5:  # leave space for logs + input
                break
            try:
                self.stdscr.addstr(y, 0, line[:w - 1])
            except curses.error:
                pass
            y += 1

        # separator line
        if y < h - 5:
            try:
                self.stdscr.addstr(y, 0, "-" * line_len)
            except curses.error:
                pass
            y += 1

        # save where logs start
        self.room_height = y
        self.log_y = y

        self.stdscr.refresh()

    def clear_logs(self):
        h, w = self.stdscr.getmaxyx()

        for y in range(self.room_height, h - 1):
            try:
                self.stdscr.move(y, 0)
                self.stdscr.clrtoeol()
            except curses.error:
                pass

        self.log_y = self.room_height
        self.stdscr.refresh()


