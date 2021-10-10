import unittest

from src.service.game import Game, GameAlreadyEndedException
from src.domain.board import Board, BoardFullColumnDropException

from test.config import settings

class GameTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(4, 4)

        self.game = Game(self.board)

    def test_game(self):
        for _ in range(3):
            self.game.make_move(0, 1)
            self.assertFalse(self.game.get_winner())

        self.game.make_move(0, 2)

        with self.assertRaises(BoardFullColumnDropException):
            self.game.make_move(0, 1)

        for _ in range(3):
            self.game.make_move(1, 2)
            self.assertFalse(self.game.get_winner())

        self.game.make_move(1, 2)
        self.assertEqual(self.game.get_winner(), 2)

        with self.assertRaises(GameAlreadyEndedException):
            self.game.make_move(0, 1)
