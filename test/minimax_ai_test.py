import unittest

from src.ai.random_ai import RandomAI
from src.ai.minimax_ai import MiniMaxAI

from src.service.game import Game
from src.domain.board import Board

from test.config import settings

def player_turn_sequence_generator():
    current_player = 1

    while True:
        yield current_player
        
        current_player = (current_player + 1) % 3

        if current_player == 0:
            current_player = 1

class NoUI_Random_VS_MinimaxController:
    def __init__(self):
        self.board = Board(7, 6)

        self.game = Game(self.board)
        self.player_turn_iterator = player_turn_sequence_generator()

    def run(self):
        while self.game.get_winner() is None:
            current_player = next(self.player_turn_iterator)

            if current_player == 1:
                move = RandomAI.get_move(self.board, current_player)
            elif current_player == 2:
                move = MiniMaxAI.get_move(self.board, current_player)

            self.game.make_move(move, current_player)

        return self.game.get_winner()

class MiniMaxAITest(unittest.TestCase):
    def setUp(self):
        self.controller = NoUI_Random_VS_MinimaxController()

        self.board = Board(7, 6)

    def test_minimax_vs_ai(self):
        minimax_wins = 0

        NUMBER_OF_GAMES = 500
        for _ in range(NUMBER_OF_GAMES):
            minimax_wins += 1 if self.controller.run() == 2 else 0

        self.assertTrue(minimax_wins / NUMBER_OF_GAMES > 0.99)

    def test_gets_game_ending_moves(self):
        horizontal = Board(7, 6)
        horizontal.drop_piece(0, 1)
        horizontal.drop_piece(1, 1)
        horizontal.drop_piece(2, 1)

        self.assertEqual(MiniMaxAI.get_move(horizontal, 1), 3)
        self.assertEqual(MiniMaxAI.get_move(horizontal, 2), 3)

        vertical = Board(7, 6)
        vertical.drop_piece(0, 1)
        vertical.drop_piece(0, 1)
        vertical.drop_piece(0, 1)

        self.assertEqual(MiniMaxAI.get_move(vertical, 1), 0)
        self.assertEqual(MiniMaxAI.get_move(vertical, 2), 0)

        positive = Board(7,6)
        positive.drop_piece(0, 1)

        positive.drop_piece(1, 2)
        positive.drop_piece(1, 1)

        positive.drop_piece(2, 2)
        positive.drop_piece(2, 2)
        positive.drop_piece(2, 1)

        positive.drop_piece(2, 2)
        positive.drop_piece(2, 3)
        positive.drop_piece(2, 2)

        self.assertEqual(MiniMaxAI.get_move(positive, 1), 3)
        self.assertEqual(MiniMaxAI.get_move(positive, 2), 3)

        negative = Board(7,6)
        negative.drop_piece(0, 2)
        negative.drop_piece(0, 2)
        negative.drop_piece(0, 2)
        negative.drop_piece(0, 1)

        negative.drop_piece(1, 2)
        negative.drop_piece(1, 2)
        negative.drop_piece(1, 1)

        negative.drop_piece(2, 3)
        negative.drop_piece(2, 1)

        self.assertEqual(MiniMaxAI.get_move(negative, 1), 3)
        self.assertEqual(MiniMaxAI.get_move(negative, 2), 3)

    def test_no_valid_moves(self):
        for column_index in range(self.board.width):
            for _ in range(self.board.height):
                self.board.drop_piece(column_index, 3)

        self.assertIsNone(MiniMaxAI.get_move(self.board, 2))
