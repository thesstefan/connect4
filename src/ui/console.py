from functools import reduce

from src.domain.board import Board
from config import settings

class ConsoleUI:
    def __init__(self):
        """ Constructs the console UI (sets up player symbols) """ 
        self.__player_to_symbol = { 0: settings["console"]["EMPTY_SYMBOL"] }

        for player in range(1, settings["game"]["NUMBER_OF_PLAYERS"] + 1):
            self.__player_to_symbol[player] = settings["console"]["PLAYER_{}_SYMBOL".format(player)]

    def draw(self, board):
        """ 
        Draws the board 

        :param board: the Board do be drawn
        :tparam board: Board
        """
        print()
        for row_index in range(settings["game"]["BOARD_HEIGHT"]):
            print("".join([self.__player_to_symbol[player] for player in board[row_index]]))
        print()

    def get_move(self, player, valid_moves):
        """
        Gets the move from the user

        :param player: the player that executed the move
        :tparam player: player id value
        """
        def get_unparsed_move():
            return input("{} ({}) -> Your move [1-{}]): ".format(
                            settings["game"]["PLAYER_{}_NAME".format(player)],
                            self.__player_to_symbol[player],
                            settings["game"]["BOARD_WIDTH"]))

        valid_input_values = [str(column + 1) for column in valid_moves]

        while (column_choice := get_unparsed_move()) not in valid_input_values:
            print("Invalid choice (Full Column / Bad Input). Try again!")
            print()

        return int(column_choice) - 1

    def make_move(self, column_choice, player):
        """
        Prints message describing move that was made

        :param column_choice: the column on which the move was made
        :tparam column_choice: nonnegative integer

        :param player: the player that made the move
        :tparam player: player id value
        """
        print("\n{} ({}) moved on column {} \n".format(
                settings["game"]["PLAYER_{}_NAME".format(player)],
                self.__player_to_symbol[player],
                column_choice + 1))

    def display_winner(self, winner):
        """
        Displays the winner

        :param winner: the winner to be displayed
        :tparam winner: player id value
        """
        print("WINNER: {} ({})".format(
            settings["game"]["PLAYER_{}_NAME".format(winner)],
            self.__player_to_symbol[winner])
        )
