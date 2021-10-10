import unittest

from src.ai.random_ai import RandomAI
from src.domain.board import Board
from test.config import settings

class RandomAITest(unittest.TestCase):
    def setUp(self):
        self.board = Board(4, 4)

    def test_random_ai(self):
        self.assertEqual(len(self.board.get_valid_moves()), 4)
        self.assertIn(RandomAI.get_move(self.board, 1), self.board.get_valid_moves())
        self.assertIn(RandomAI.get_move(self.board, 2), self.board.get_valid_moves())

        for _ in range(4):
            self.board.drop_piece(0, 1)
        self.assertEqual(len(self.board.get_valid_moves()), 3)
        self.assertIn(RandomAI.get_move(self.board, 2), self.board.get_valid_moves())

        for _ in range(4):
            self.board.drop_piece(1, 2)
        self.assertEqual(len(self.board.get_valid_moves()), 2)
        self.assertIn(RandomAI.get_move(self.board, 2), self.board.get_valid_moves())

        for _ in range(4):
            self.board.drop_piece(2, 3)
        self.assertEqual(len(self.board.get_valid_moves()), 1)
        self.assertIn(RandomAI.get_move(self.board, 2), self.board.get_valid_moves())

        for _ in range(4):
            self.board.drop_piece(3, 4)
        self.assertEqual(len(self.board.get_valid_moves()), 0)
        self.assertIsNone(RandomAI.get_move(self.board, 2))
