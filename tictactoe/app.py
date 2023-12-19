# -*- coding: utf-8 -*-

_INTRO = """
╔╦╗┬┌─┐╔╦╗┌─┐┌─┐╔╦╗┌─┐┌─┐
 ║ ││   ║ ├─┤│   ║ │ │├┤
 ╩ ┴└─┘ ╩ ┴ ┴└─┘ ╩ └─┘└─┘

How to Play:
    Each player takes turns entering a character on the playing board.
    To win, a player must match 3 characters in a row, column or crosswise pattern.

Credits: Jesse Stippel
"""

from logging import Logger  # noqa: E402
from os import environ

_log = Logger(__name__)

BOARD = """
{0} | {1} | {2}
---------
{3} | {4} | {5}
---------
{6} | {7} | {8}
"""


def validate_moves(func):
    """Validate move and check if char already added."""

    def wrapper(*args, **kwargs):
        app, player, char, pos = args
        if app.board[pos] is not None:
            _log.warning("This position is already taken!")
            return
        return func(app, player, char, pos)

    return wrapper


def check_winners(func):
    """Check if the last turn is a winning move."""

    def wrapper(*args, **kwargs):
        app, player, char, pos = args
        retval = func(app, player, char, pos)
        if app.turns >= 5:
            # Return all columns, rows and crosswise positions.
            idxs = app.get_columns() + app.get_rows() + app.get_crosswise()
            # Return all the player unicode values for comparison.
            player_ords = [int(_) for _ in app._players]
            for maxval, _ in idxs:
                # If one of the position groups evaluates to the player maxval,
                # we assume that all characters are the same and we have a winner.
                if maxval in player_ords:
                    app.has_winner = (True, maxval, _)
                    player = app.get_player(maxval)
                    player.wins += 1
                    print(f"{player._name} has won!")
                    break
            return retval

    return wrapper


class Player:
    """Player class with basic metadata."""

    wins: int = 0

    _name: str
    _char: str
    _maxval: int

    def __init__(self, char: str, *args, **kwargs):
        self._char = char
        self._name = f"Player {self._char.upper()}"
        self._maxval = ord(self._char) * 3

    def __repr__(self):
        # Make the class easier to visually grep.
        return f"{self.__class__.__name__}({self._char.upper()}, {self._maxval})"

    def __int__(self):
        # If encapsulating with int, return the unicode value.
        return self._maxval


class TicTacToeApp:
    """The TicTacToeApp base class."""

    test_mode: bool = False

    board: dict = {}
    turns: int = 0
    has_winner: tuple = (False, None, None)

    last_turn: tuple = ()
    next_turn: Player = object

    _players: list = []

    def __init__(self, chars: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(_INTRO)
        # We need 2 characters to play.
        if len(chars) != 2:
            raise ValueError("A min:max of 2 characters are required to play.")
        # Append players with chosen characters.
        for char in chars:
            self._players.append(Player(char))
        # Reset the board to default.
        self.reset_board()
        # Assign the starting player.
        self.next_turn = self._players[0]
        # Skip interactive step for running app in test mode.
        if environ.get('TICTACTOE_TEST') == "true":
            self.test_mode = True
            return
        # Print an intro dialogue.
        start = input("Are you ready to start the game? y/n: ")
        if not self.is_yes(start):
            exit()
        # Start the game.
        self.start_game()

    def start_game(self):
        """Start the game loop until a winner is found."""
        self.print_board(self.board)
        # Start the game loop until turns are exhausted or a winner is found.
        while self.turns <= 8:
            pos = input(f"{self.next_turn._name} enter a position: ")
            self.insert_value(self.next_turn, self.next_turn._char, int(pos))
            if self.has_winner[0]:
                cont = input("Continue playing? y/n: ")
                if not self.is_yes(cont):
                    msg = ""
                    for player in self.players:
                        msg += f"{player._name} wins: {player.wins}\n"
                    print(msg)
                    exit()
                self.reset_board()
                self.start_game()
            self.print_board(self.board)

    def is_yes(self, value: str):
        """Checks if input value is confirmation."""
        confirm = "yes"
        confirms = [
            confirm,
            confirm.upper(),
            confirm.capitalize(),
            confirm[0],
            confirm[0].upper(),
        ]
        if value in confirms:
            return True
        return False

    def print_board(self, board: dict):
        args = []
        for value in board:
            args.append(board[value] or value)
        output = BOARD.format(*args)
        print(output)
        return output

    def reset_board(self):
        """Resets the playing board to default."""
        # Reset the player turns to 0.
        self.turns = 0
        self.has_winner = (False, None, None)
        self.next_turn = self._players[0]
        # Reset the board to default.
        self.board = dict(enumerate([None] * 9, start=1))
        _log.warning("The playing board has been reset.")

    def get_board_values(self, idxs: tuple) -> tuple:
        # Instead of matching all of the characters with a
        # given index, we match the sum of the unicode representation.
        # This gives us a single value to compare against.
        value = 0
        for num in idxs:
            bval = self.board[num]
            if bval is not None:
                value += ord(bval)
        return value, idxs

    def get_columns(self) -> list:
        idxs = [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
        return [self.get_board_values(_idxs) for _idxs in idxs]

    def get_rows(self) -> list:
        idxs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        return [self.get_board_values(_idxs) for _idxs in idxs]

    def get_crosswise(self) -> list:
        idxs = [(1, 5, 9), (3, 5, 7)]
        return [self.get_board_values(_idxs) for _idxs in idxs]

    @check_winners
    @validate_moves
    def insert_value(self, player: object, value: str, pos: int):
        # Insert the character into the board at position ...
        self.board[pos] = value
        # Assign the current move to the last_turn attribute.
        self.last_turn = (player, value, pos)
        # Assign the next player in the series.
        self.next_turn = next((_ for _ in self._players if _._maxval != player._maxval))
        self.turns += 1

    @property
    def columns(self):
        return self.get_columns()

    @property
    def rows(self):
        return self.get_rows()

    @property
    def crosswise(self):
        return self.get_crosswise()

    @property
    def players(self):
        return self._players

    def get_player(self, ord):
        """Return a player object using the unicode value."""
        for player in self.players:
            if int(player) == ord:
                return player
