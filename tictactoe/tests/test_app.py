# -*- coding: utf-8 -*-

import unittest
from tictactoe import create_app
from unittest import mock


class TestTicTacToeApp(unittest.TestCase):
    """Tests for the TicTacToeApp."""

    def test_init(self):
        self.app = create_app()
        self.assertEqual(len(self.app.players), 2)
        player_chars = [_._char for _ in self.app.players]
        self.assertIn("x", player_chars)
        self.assertIn("o", player_chars)

    def test_is_yes(self):
        self.app = create_app()
        self.assertTrue(self.app.is_yes("y"))
        self.assertTrue(self.app.is_yes("yes"))
        self.assertFalse(self.app.is_yes("n"))
        self.assertFalse(self.app.is_yes("foo"))

    def test_print_board(self):
        self.app = create_app()
        output = self.app.print_board(self.app.board)
        self.assertNotIn("x", output)
        self.assertNotIn("y", output)
        self.app.insert_value(self.app.next_turn, self.app.next_turn._char, 1)
        output_ins = self.app.print_board(self.app.board)
        self.assertIn("x", output_ins)

    def test_insert_value(self):
        self.app = create_app()
        self.assertEqual(self.app.turns, 0)
        self.assertEqual(self.app.next_turn._char, "x")
        self.app.insert_value(self.app.next_turn, self.app.next_turn._char, 1)
        self.assertEqual(self.app.turns, 1)
        self.assertEqual(self.app.next_turn._char, "o")

    def test_reset_board(self):
        self.app = create_app()
        self.app.turns = 1
        self.app.has_winner = (True, 360, (1, 4, 7))
        self.app.next_turn = self.app.players[1]
        self.app.board = {
            1: "x",
            2: "o",
            3: "o",
            4: "x",
            5: None,
            6: None,
            7: "x",
            8: None,
            9: None,
        }
        self.app.reset_board()
        self.assertEqual(self.app.turns, 0)
        self.assertEqual(self.app.has_winner, (False, None, None))
        self.assertEqual(self.app.next_turn, self.app.players[0])
        board_vals = self.app.board.values()
        self.assertNotIn("x", board_vals)
        self.assertNotIn("o", board_vals)
