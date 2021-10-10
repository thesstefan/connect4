from src.controller.master_controller import MasterController

from src.domain.board import Board
from src.service.game import Game

from src.ai.random_ai import RandomAI
from src.ai.minimax_ai import MiniMaxAI

from src.ui.console import ConsoleUI
from src.ui.graphical import PyGameUI

from config import settings

class MasterControllerFactory:
    """ Creates basic MasterController using the provided settings """

    @staticmethod
    def get_ai_engine():
        return MiniMaxAI if settings["game"]["USE_MINIMAX"] else RandomAI

    @staticmethod
    def get_ui():
        return PyGameUI() if settings["game"]["USE_GUI"] else ConsoleUI()

    @staticmethod
    def get_controller():
        board = Board(settings["game"]["BOARD_WIDTH"],
                      settings["game"]["BOARD_HEIGHT"])
        game = Game(board)

        return MasterController(
                board,
                game,
                MasterControllerFactory.get_ai_engine(),
                MasterControllerFactory.get_ui(),
                settings["game"]["AI_PLAYERS"]
        )

if __name__ == "__main__":
    controller = MasterControllerFactory.get_controller()
    controller.run()
