from src.domain.board import Board
from src.service.game_state_analyzer import GameStateAnalyzer

from config import settings

class GameException(Exception):
    """ General Exception raised by Game """
    pass

class GameAlreadyEndedException(GameException):
    """ 
    Raised by Game when a move is attempted after a 
    winner is already chosen
    """
    pass

class Game:
    """ Basic game interface. Implements move making and winner checking. """

    def __init__(self, board):
        """
        Initialises Game instance.

        :param board: the Board instance to be used
        :tparam board: Board
        """
        self.__board = board
        self.__winner = None

    def make_move(self, column_index, player):
        """ 
        Makes a move (drops a piece in the given column)

        :param column_index: the index of the column where the move is made
        :tparam column_index: nonnegative integer

        :param player: the player that makes the move
        :tparam player: player id value

        :raises: GameAlreadyEndedException if a winner was already determined
        :raises: BoardFullColumnDropException if column is already chosen
        """
        if self.__winner:
            raise GameAlreadyEndedException

        self.__board.drop_piece(column_index, player)
        self.__winner = player if GameStateAnalyzer.is_player_winning(self.__board, player)  \
                        else None

    def get_winner(self):
        """ Returns the winner of the game / None """
        return self.__winner
