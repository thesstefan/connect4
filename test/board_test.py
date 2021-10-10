import unittest

from src.domain.board import Board, BoardFullColumnDropException
from test.config import settings

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(4, 4)

    def test_constructor_getitem(self):
        self.assertFalse(self.board[:].all())

        for row_index in range(self.board.height):
            for column_index in range(self.board.width):
                self.assertEqual(self.board[row_index][column_index], 0)

    def test_drop_piece(self):
        for _ in range(4):
            self.board.drop_piece(0, 1)

        for row_index in range(self.board.height):
            self.assertEqual(self.board[row_index][0], 1)

        with self.assertRaises(BoardFullColumnDropException):
            self.board.drop_piece(0, 1)

    def test_get_top_occupied_row_index(self):
        for _ in range(4):
            self.board.drop_piece(0, 1)

        for row_index in range(self.board.height):
            self.assertEqual(self.board[row_index][0], 1)

        self.assertEqual(self.board.get_top_occupied_row_index(0), 0)
        self.assertEqual(self.board.get_top_occupied_row_index(1), 4)

        self.board.drop_piece(2, 1)
        self.assertEqual(self.board.get_top_occupied_row_index(2), 3)

    def test_is_valid_move(self):
        for _ in range(4):
            self.board.drop_piece(0, 1)

        self.board.drop_piece(2, 1)

        for row_index in range(self.board.height):
            self.assertEqual(self.board[row_index][0], 1)

        self.assertFalse(self.board.is_valid_move(0))
        self.assertTrue(self.board.is_valid_move(1))
        self.assertTrue(self.board.is_valid_move(2))
        self.assertTrue(self.board.is_valid_move(3))

    def test_get_valid_moves(self):
        for _ in range(3):
            self.board.drop_piece(0, 1)

        self.assertEqual(len(self.board.get_valid_moves()), 4)

        self.board.drop_piece(0, 1)
        self.assertEqual(len(self.board.get_valid_moves()), 3)
        self.assertNotIn(0, self.board.get_valid_moves())
