import time


class PuzzleHandler:
    """
    Handles solving puzzles in the game.
    """
    def __init__(self, ui, player):
        self.ui = ui
        self.player = player

    def check_solution(self, answer):
        """
        Checks the answer against the puzzle's solution.
        :param answer: The attempted answer given by the player.
        :return: True if the answer is the solution, False otherwise.
        """
        return answer == self.player.current_room.puzzle.solution

    def do_solve(self):
        """
        Attempt to solve the puzzle in the current room.
        :return: None
        """
        room = self.player.current_room
        puzzle = room.puzzle

        if puzzle is None:
            self.ui.display_text("There is no puzzle here.")
            return

        if puzzle.solved:
            self.ui.display_text("You have already solved this puzzle.")

        # show the puzzle is opening
        self.ui.display_text(f"{puzzle.name} opening", end="")
        for i in range(3):
            time.sleep(0.5)
            self.ui.display_text(".", end="")
        self.ui.display_text("")
        time.sleep(0.5)

        # solving loop
        while not puzzle.solved:
            self.ui.clear_logs()
            self.ui.display_text(puzzle.prompt)
            answer = self.ui.get_text()  # retrieve answer from user

            if self.check_solution(answer):
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
            self.handle_puzzle_reward(puzzle.reward, room)

    def handle_puzzle_reward(self, reward, room):
        """
        Handles the reward from the puzzle.
        :param reward: The reward given from the puzzle.
        :param room: The room that the player is currently in -
        reward is dropped if player's storage is too small to hold it.
        :return: None
        """
        self.ui.display_text(f"You have received: {reward.name}")
        prev_weight = self.player.weight
        picked_up = self.player.pick_up(reward)
        if picked_up:
            self.ui.display_text(f"{reward.name} added to storage.")
            self.ui.display_text(f"Storage: {prev_weight} + {reward.weight} --> "
                                 f"{self.player.weight}/{self.player.max_weight} bytes")

        if not picked_up:
            room.add_item(reward)
            self.ui.display_text(f"{reward.name} has fallen to the floor.")
