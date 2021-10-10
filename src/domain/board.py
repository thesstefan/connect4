import numpy as np

class BoardException(Exception):
    """ General exception raised by Board """
    pass

class BoardFullColumnDropException(BoardException):
    """ 
    Exception raised by Board when something (user/ai/...)
    attempts to drop a piece into an already full column
    """
    pass

class Board:
    """
    Basic implementation of Connect 4 board. 
    (matrix of pieces, with the ability to "drop" pieces into a column)
    """

    def __init__(self, width, height):
        """
        Initializes the Board instance.
        (empty board contains 0 in all positions)

        :param width: the width of the Board
        :tparam width: positive integer 

        :param height: the height of the Board
        :tparam width: positive integer 

        :tparam: value from piece_types dict
        """
        self.__board = np.zeros((height, width))

    def __getitem__(self, row_index):
        """
        Returns a row of the Board.

        :param row_index: the index of the row to be returned
        :tparam row_index: nonnegative integer

        :returns: list of values from piece_types dict
        """
        return self.__board[row_index]

    def drop_piece(self, column_index, player_id):
        """
        Drops a piece into the Board.
        (fills the top empty space in a column with the given piece type)

        :param column_index: the column where the piece should be dropped
        :tparam column_index: nonnegative integer

        :param player_id: the id of the player that dropped the piece
        :tparam player_id: nonnegative integer

        :raises: BoardFullColumnDropException on full column drop attempt
        """
        for row_index in range(self.__board.shape[0] - 1, -1, -1):
            if self.__board[row_index][column_index] == 0:
                self.__board[row_index][column_index] = player_id

                return

        raise BoardFullColumnDropException

    def get_top_occupied_row_index(self, column_index):
        """
        Returns the index of the top occupied row on a given column

        :param column_index: the column to look by
        :tparam column_index: nonnegative integer

        :returns: the index of the top occupied row
        :rtype: positive integer
        """
        for row_index in range(0, self.__board.shape[0]):
            if self.__board[row_index][column_index] != 0:
                return row_index

        return self.__board.shape[0]

    def is_valid_move(self, column_index):
        """ 
        Checks if a piece can be dropped in a given column
        (checks if the column is full)

        :param column_index: the column to look into
        :tparam column_index: nonnegative integer
        """
        return self.__board[0][column_index] == 0 

    def get_valid_moves(self):
        """
        Returns the list of valid moves

        :rtype: list of nonnegative integers
        """
        return list(filter(self.is_valid_move, range(self.__board.shape[1])))

    @property
    def height(self):
        """ Returns the height of the Board """
        return self.__board.shape[0]

    @property
    def width(self):
        """ Returns the width of the Board """
        return self.__board.shape[1]
