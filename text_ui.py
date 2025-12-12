import curses

class TextUI:
    """A simple text based User Interface (UI) for the game."""
    def __init__(self):
        self.stdscr = None
        self.started = False

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

    def print(self, text, y=None, x=0):
        if y is None:
            y, _ = self.stdscr.getyx()

        for line in str(text).split("\n"):
            self.stdscr.addstr(y, x, line)
            y += 1

        self.stdscr.refresh()

        # -----------------------------
        # INPUT
        # -----------------------------

    def get_key(self):
        key = self.stdscr.getch()
        self.stdscr.addstr(0, 0, f"Key code: {key}   ")
        self.stdscr.refresh()
        return key

    def get_text(self, prompt="> "):
        curses.echo()
        self.print(prompt)
        y, x = self.stdscr.getyx()
        text = self.stdscr.getstr(y, x).decode("utf-8")
        curses.noecho()
        return text
