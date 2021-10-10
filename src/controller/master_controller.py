from random import choice

from src.domain.board import Board
from src.service.game import Game
from src.ui.console import ConsoleUI
from src.ui.graphical import PyGameUI
from src.ai.random_ai import RandomAI
from src.ai.minimax_ai import MiniMaxAI

from config import settings

def player_turn_sequence_generator():
    """ 
    Generator function for player turn switching

    Iterates over the [1, NUMBER_OF_PLAYERS] players
    """
    current_player = 1

    while True:
        yield current_player
        
        current_player = (current_player + 1) % (settings["game"]["NUMBER_OF_PLAYERS"] + 1)

        if current_player == 0:
            current_player = 1

class MasterController:
    """
    Main dispatcher of the program. Connects UI, AI and Game.
    """

    def __init__(self, board, game, ai_engine, ui, ai_players):
        """ Initializes the Board, UI, AI and turn iterator """
        self.__board = board
        self.__game = game
        self.__ai_engine = ai_engine
        self.__ui = ui 

        self.__ai_players = ai_players
        self.__player_turn_iterator = player_turn_sequence_generator()

    def run(self):
        """ Runs the game loop """
        while self.__game.get_winner() is None:
            self.__ui.draw(self.__board)

            current_player = next(self.__player_turn_iterator)

            if "PLAYER_{}".format(current_player) in self.__ai_players:
                column_choice = self.__ai_engine.get_move(self.__board, current_player)
            else:
                column_choice = self.__ui.get_move(current_player, self.__board.get_valid_moves())

            self.__ui.make_move(column_choice, current_player)
            self.__game.make_move(column_choice, current_player)

        self.__ui.draw(self.__board)
        self.__ui.display_winner(self.__game.get_winner())
