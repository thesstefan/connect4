import unittest
from copy import deepcopy

from test.config import settings

from src.domain.board import Board
from src.service.game import Game
from src.ai.random_ai import RandomAI
from src.controller.master_controller import MasterController

class WinnerException(Exception):
    def __init__(self, winner):
        self.winner = winner

class FakeUI():
    def make_move(self, _x, _y):
        pass
    
    def draw(self, _x):
        pass

    def get_move(self, _x, _y):
        pass

    def display_winner(self, winner):
        raise WinnerException(winner)

class MasterControllerTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(7, 6)
        self.game = Game(self.board)
        self.ui = FakeUI()
        self.ai_engine = RandomAI

        ai_players = settings["game"]["AI_PLAYERS"]
        self.controller = MasterController(self.board, self.game, self.ai_engine, self.ui, ai_players)

    def test_run(self):
        try:
            self.controller.run()
        except WinnerException as winner_ex:
            self.assertEqual(winner_ex.winner, self.game.get_winner())
