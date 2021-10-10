from copy import deepcopy
from math import inf
from random import choice

from src.service.game_state_analyzer import GameStateAnalyzer
from config import settings

class MiniMaxAI:
    """ 
    Implements AI decision making using the minimax algorithm paired with the
    alpha beta pruning search technique

    Currently supports only WINNING_SEQUENCE_LENGTH=4 and one opponent
    (use with 2 players)
    """

    """ The score given assigned to an AI move when it wins the game """
    WINNING_SCORE = 999_999
    """ The score given assigned to an AI move when it loses the game """
    LOSING_SCORE = -999_999

    """ The index of the column in the minimax return tuple """
    COLUMN_INDEX = 0
    """ The index of the score in the minimax return tuple """
    SCORE_INDEX = 1

    @staticmethod
    def get_move(board, player):
        """ 
        Returns the move of the AI using the alpha-beta pruning minimax algorithm

        :param board: the Board to be used
        :tparam board: Board

        :param player: the player represented by the AI
        :tparam player: player score id

        :return: chosen move column
        :rtype: nonnegative integer
        """
        return MiniMaxAI.__minimax(
                board, player, settings["ai"]["minimax"]["DEPTH"], -inf, inf, True
        )[MiniMaxAI.COLUMN_INDEX]

    @staticmethod
    def __get_opponent(player):
        """ 
        Returns the opponent of a player 

        Supports only one opponent
        """
        opponent_player = (player + 1) % (settings["game"]["NUMBER_OF_PLAYERS"] + 1)
        if opponent_player == 0:
            opponent_player = 1

        return opponent_player

    @staticmethod
    def __maximize(board, player, depth, alpha, beta):
        """ Maximizes the score of the AI player """
        score = -inf
        chosen_column_index = choice(board.get_valid_moves())

        for column_index in board.get_valid_moves():
            board_copy = deepcopy(board)
            board_copy.drop_piece(column_index, player)

            new_score = MiniMaxAI.__minimax(
                board_copy, player, depth - 1, alpha, beta, False
            )[MiniMaxAI.SCORE_INDEX]

            """ No more messing around (find a better way) """
            if depth == settings["ai"]["minimax"]["DEPTH"] and new_score == MiniMaxAI.WINNING_SCORE:
                for winning_column_index in board.get_valid_moves():
                    board_copy = deepcopy(board)
                    board_copy.drop_piece(winning_column_index, player)
                    
                    if GameStateAnalyzer.is_player_winning(board_copy, player):
                        return winning_column_index, MiniMaxAI.WINNING_SCORE

            if new_score > score:
                score = new_score
                chosen_column_index = column_index

            alpha = max(alpha, score)

            if alpha >= beta:
                break

        return chosen_column_index, score 

    @staticmethod
    def __minimize(board, player, depth, alpha, beta):
        """ Minimizes the score of the opponent of the AI player """
        score = inf
        chosen_column_index = choice(board.get_valid_moves())

        for column_index in board.get_valid_moves():
            board_copy = deepcopy(board)
            board_copy.drop_piece(column_index, MiniMaxAI.__get_opponent(player))

            new_score = MiniMaxAI.__minimax(
                board_copy, player, depth - 1, alpha, beta, True
            )[MiniMaxAI.SCORE_INDEX]

            if new_score < score:
                score = new_score
                chosen_column_index = column_index

            beta = min(beta, score)

            if alpha >= beta:
                break

        return chosen_column_index, score

    @staticmethod
    def __evaluate_sequence(sequence, player):
        """ Gives a score to a sequence """
        if sequence.count(player) == 3 and sequence.count(0) == 1:
            return settings["ai"]["minimax"]["EVALUATE_SEQUENCE_SCORES"][1]
        elif sequence.count(player) == 2 and sequence.count(0) == 2:
            return settings["ai"]["minimax"]["EVALUATE_SEQUENCE_SCORES"][2]
        elif sequence.count(MiniMaxAI.__get_opponent(player)) == 3 and sequence.count(0) == 1:
            return settings["ai"]["minimax"]["EVALUATE_SEQUENCE_SCORES"][3]

        return 0

    @staticmethod
    def __score_position(board, player):
        """ Gets a score for the game state of the current node """
        score = 0

        center_array = list(board[:, settings["game"]["BOARD_WIDTH"] // 2])
        center_count = center_array.count(player)
        score += center_count * settings["ai"]["minimax"]["CENTER_ARRAY_SCORE_MULTIPLIER"] 

        winning_sequence_length = settings["game"]["WINNING_SEQUENCE_LENGTH"]

        """ Horizontal """
        for row_index in range(board.height):
            row_array = list(board[row_index, :])

            for column_index in range(board.width - winning_sequence_length + 1):
                sequence = row_array[column_index:column_index + winning_sequence_length]
                score += MiniMaxAI.__evaluate_sequence(sequence, player)

        """ Vertical """
        for column_index in range(board.width):
            column_array = list(board[:, column_index])

            for row_index in range(board.height - winning_sequence_length + 1):
                sequence = column_array[row_index:row_index + winning_sequence_length]
                score += MiniMaxAI.__evaluate_sequence(sequence, player)

        """ Positive slope diagonals """
        for row_index in range(board.height - winning_sequence_length + 1):
            for column_index in range(board.width - winning_sequence_length + 1):
                sequence = [board[row_index + sequence_index][column_index + sequence_index] 
                        for sequence_index in range(winning_sequence_length)] 
                score += MiniMaxAI.__evaluate_sequence(sequence, player)

        """ Negative slope diagonals """
        for row_index in range(board.height - winning_sequence_length + 1):
            for column_index in range(board.width - winning_sequence_length + 1):
                sequence =              \
                [board[row_index - winning_sequence_length + 1 - sequence_index][column_index + sequence_index] 
                        for sequence_index in range(winning_sequence_length)] 
                score += MiniMaxAI.__evaluate_sequence(sequence, player)

        return score

    @staticmethod
    def __minimax(board, player, depth, alpha, beta, maximizing_player):
        """ Minimax algorithm """
        if GameStateAnalyzer.is_player_winning(board, player):
            return (None, MiniMaxAI.WINNING_SCORE)
        if GameStateAnalyzer.is_player_winning(board, MiniMaxAI.__get_opponent(player)):
            return (None, MiniMaxAI.LOSING_SCORE)
        if not board.get_valid_moves():
            return (None, 0)
        if depth == 0:
            return (None, MiniMaxAI.__score_position(board, player))

        if maximizing_player:
            return MiniMaxAI.__maximize(board, player, depth, alpha, beta)

        return MiniMaxAI.__minimize(board, player, depth, alpha, beta)
