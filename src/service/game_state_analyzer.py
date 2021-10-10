from config import settings

class GameStateAnalyzer:
    @staticmethod
    def __is_winning_4_sequence(sequence, player):
        """ 
        Checks if a sequence is a winning sequence for the given player
        A sequence is a winning sequence for a player if it 
            contains 4 of its pieces

        :param sequence: the sequence to be checked
        :tparam sequence: iterable with hashable values
                          usually list of ints

        :param player: the player to be checked as the winner
        :tparam player: player id value

        :returns: True if the given sequence is winning for the player
                  False otherwise
        """
        piece_set = {*sequence}

        return len(piece_set) == 1 and player in piece_set 

    @staticmethod 
    def is_player_winning(board, player):
        """ 
        Check if the given players wins the game by searching
        the board for winning sequences.

        :param board: the board to be checked

        :param player: the player to be checked as the winner
        :tparam player: player id value

        :returns: True if the given player wins, False otherwise
        """
        winning_sequence_length = settings["game"]["WINNING_SEQUENCE_LENGTH"]

        """ Check horizontal """
        for column in range(board.width - winning_sequence_length + 1):
            for row in range(board.height):
                if GameStateAnalyzer.__is_winning_4_sequence(
                    [board[row][column + index] for index in range(winning_sequence_length)], 
                    player
                ):
                    return True

        """ Check vertical"""
        for column in range(board.width):
            for row in range(board.height - winning_sequence_length + 1):
                if GameStateAnalyzer.__is_winning_4_sequence(
                    [board[row + index][column] for index in range(winning_sequence_length)], 
                    player
                ):
                    return True

        """ Check positive slope """
        for column in range(board.width - winning_sequence_length + 1):
            for row in range(board.height - winning_sequence_length + 1):
                if GameStateAnalyzer.__is_winning_4_sequence(
                    [board[row + index][column + index] for index in range(winning_sequence_length)],
                    player
                ):
                    return True

        """ Check negative slope """
        for column in range(board.width - winning_sequence_length + 1):
            for row in range(board.height):
                if GameStateAnalyzer.__is_winning_4_sequence(
                    [board[row - index][column + index] for index in range(winning_sequence_length)],
                    player
                ):
                    return True

        return False
