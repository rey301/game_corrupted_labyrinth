import time

class Solver:
    def __init__(self, ui, player, game):
        self.ui = ui
        self.player = player
        self.game = game

    def do_solve(self):
        """Attempt to solve the puzzle in the current room."""
        room = self.player.current_room
        puzzle = room.puzzle

        if puzzle is None:
            self.ui.display_text("There is no puzzle here.")
            return

        if puzzle.solved:
            self.ui.display_text("You have already solved this puzzle.")

        self.ui.display_text(f"{puzzle.name} opening", end="")
        for i in range(3):
            time.sleep(0.5)
            self.ui.display_text(".", end="")
        self.ui.display_text("")
        time.sleep(0.5)
        while not puzzle.solved:
            self.ui.clear_logs()
            self.ui.display_text(puzzle.prompt)
            answer = self.ui.get_inp()# retrieve answer from user

            if answer == puzzle.solution:
                puzzle.solved = True
                self.ui.clear_logs()
                self.ui.display_text("Engram has broken, it fizzles into air.")
            else:
                self.ui.display_text("Incorrect. Try again.")
            time.sleep(0.5)

        self.ui.clear_logs()

        if room.puzzle.solved:
            room.remove_puzzle()

        if puzzle.reward:
            self._handle_puzzle_reward(puzzle.reward, room)

    def _handle_puzzle_reward(self, reward, room):
        """Handle reward from solving a puzzle."""
        self.ui.display_text(f"You have received: {reward.name}")
        msg, picked_up = self.player.pick_up(reward, ui=self.ui)
        self.ui.display_text(msg)

        if not picked_up:
            room.add_item(reward)
            self.ui.display_text(f"{reward.name} has fallen to the floor.")