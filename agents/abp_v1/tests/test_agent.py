import math

import pytest
from gym_gomoku import GomokuState, Board, Color

from agents.abp_v1.agent import ABP


def to_i(x, y, dim=9):
    return Board(dim).coord_to_action(x, y)


# All boards should be 9x9
test_cases = [
    ("""
.........
.........
.........
..X.XX...
.........
.........
.........
.........
.........""", {to_i(3, 3)}),
    ("""
.........
.........
.........
.OO.OO...
.........
.........
.........
.........
.........""", {to_i(3, 3)}),
    ("""
.........
.........
.........
..XXXX...
.........
.........
.........
.........
.........""", {to_i(3, 1), to_i(3, 6)}),
    ("""
.........
.........
.........
.........
.........
.........
.........
.........
.........""", {to_i(4, 4)}),
]


def str_to_board(s):
    s = s.replace("\n", "").lower()
    dim = math.sqrt(len(s))
    assert dim == int(dim)
    board = Board(int(dim))
    for i, c in enumerate(s):
        if c in {"x", "o"}:
            board = board.play(i, Color.black if c == "x" else Color.white)
    return board


@pytest.mark.parametrize("board_str,exp_moves", test_cases)
def test_agent(board_str, exp_moves):
    board = str_to_board(board_str)
    state = GomokuState(board, Color.black)

    move = ABP(None).move(state)

    assert move in exp_moves
