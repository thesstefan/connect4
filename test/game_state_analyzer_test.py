import unittest

from src.domain.board import Board, BoardFullColumnDropException
from src.service.game_state_analyzer import GameStateAnalyzer

from test.config import settings

class GameStateAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.empty = Board(4, 4)

        self.vertical = Board(4, 4)
        self.vertical.drop_piece(0, 1)
        self.vertical.drop_piece(0, 1)
        self.vertical.drop_piece(0, 1)
        self.vertical.drop_piece(0, 1)

        self.horizontal = Board(4, 4)
        self.horizontal.drop_piece(0, 1)
        self.horizontal.drop_piece(1, 1)
        self.horizontal.drop_piece(2, 1)
        self.horizontal.drop_piece(3, 1)

        self.positive_slope = Board(4, 4)
        self.positive_slope.drop_piece(0, 1)

        self.positive_slope.drop_piece(1, 2)
        self.positive_slope.drop_piece(1, 1)

        self.positive_slope.drop_piece(2, 2)
        self.positive_slope.drop_piece(2, 2)
        self.positive_slope.drop_piece(2, 1)

        self.positive_slope.drop_piece(3, 2)
        self.positive_slope.drop_piece(3, 2)
        self.positive_slope.drop_piece(3, 2)
        self.positive_slope.drop_piece(3, 1)

        self.negative_slope = Board(4, 4)
        self.negative_slope.drop_piece(0, 2)
        self.negative_slope.drop_piece(0, 2)
        self.negative_slope.drop_piece(0, 2)
        self.negative_slope.drop_piece(0, 1)

        self.negative_slope.drop_piece(1, 2)
        self.negative_slope.drop_piece(1, 2)
        self.negative_slope.drop_piece(1, 1)

        self.negative_slope.drop_piece(2, 2)
        self.negative_slope.drop_piece(2, 1)

        self.negative_slope.drop_piece(3, 1)

    def test_game_state_analyzer(self):
        self.assertFalse(GameStateAnalyzer.is_player_winning(self.empty, 1))
        self.assertFalse(GameStateAnalyzer.is_player_winning(self.empty, 2))

        self.assertTrue(GameStateAnalyzer.is_player_winning(self.horizontal, 1))
        self.assertFalse(GameStateAnalyzer.is_player_winning(self.horizontal, 2))

        self.assertTrue(GameStateAnalyzer.is_player_winning(self.vertical, 1))
        self.assertFalse(GameStateAnalyzer.is_player_winning(self.vertical, 2))

        self.assertTrue(GameStateAnalyzer.is_player_winning(self.positive_slope, 1))
        self.assertFalse(GameStateAnalyzer.is_player_winning(self.positive_slope, 2))

        self.assertTrue(GameStateAnalyzer.is_player_winning(self.negative_slope, 1))
        self.assertFalse(GameStateAnalyzer.is_player_winning(self.negative_slope, 2))
