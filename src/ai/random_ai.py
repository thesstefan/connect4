from random import choice

from src.domain.board import Board

class RandomAI:
    """ Implements random choice AI """

    @staticmethod
    def get_move(board, player=0):
        """
        Returns random move that can be made on a given board.

        :param board: the board to be considered
        :tparam board: Board

        :return: move column index / None if no choice is available
        :rtype: nonnegative integer / None
        """
        return choice(board.get_valid_moves()) if board.get_valid_moves() else None
