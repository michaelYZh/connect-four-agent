from arena.board import Board, RED, YELLOW
from arena.player import Player


class Game:
    """
    A Game consists of a Board and 2 players
    """

    def __init__(self, model_red: str, model_yellow: str):
        """
        Initialize this Game; a new board, and new Player objects
        """
        self.board = Board()
        self.players = {
            RED: Player(model_red, RED),
            YELLOW: Player(model_yellow, YELLOW),
        }

    def reset(self):
        """
        Restart the game by resetting the board; keep players the same
        """
        self.board = Board()

    def move(self):
        """
        Make the next move. Delegate to the current player to make a move on this board.
        """
        self.players[self.board.player].move(self.board)

    def is_active(self) -> bool:
        """
        Return true if the game hasn't yet ended
        """
        return self.board.is_active()

    def thoughts(self, player) -> str:
        """
        Return the inner thoughts of the given player
        """
        return self.players[player].thoughts()

    def run(self):
        """
        If being used outside gradio; move and print in a loop
        """
        while self.is_active():
            self.move()
            print(self.board)
