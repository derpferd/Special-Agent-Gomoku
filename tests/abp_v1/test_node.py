import pytest
from gym_gomoku import GomokuState, Board, Color

from agents.abp_v1.agent import Node


@pytest.mark.parametrize("pos,direction,res", [
    (0, 0, [0, 1, 2, 3, 4]),
    (9, 0, [5, 6, 7, 8, 9]),
    (19, 0, [15, 16, 17, 18, 19]),
    (5, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    (4, 0, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
    (54, 0, [50, 51, 52, 53, 54, 55, 56, 57, 58]),

    (0, 1, [0, 10, 20, 30, 40]),
    (90, 1, [90, 80, 70, 60, 50]),
    (91, 1, [91, 81, 71, 61, 51]),
    (50, 1, [90, 80, 70, 60, 50, 40, 30, 20, 10]),
    (40, 1, [80, 70, 60, 50, 40, 30, 20, 10, 0]),
    (41, 1, [81, 71, 61, 51, 41, 31, 21, 11, 1]),
    (54, 1, [94, 84, 74, 64, 54, 44, 34, 24, 14]),

    (0, 2, [0, 11, 22, 33, 44]),
    (9, 2, [9]),
    (19, 2, [19, 8]),
    (29, 2, [29, 18, 7]),
    (55, 2, [99, 88, 77, 66, 55, 44, 33, 22, 11]),
    (44, 2, [88, 77, 66, 55, 44, 33, 22, 11, 00]),
    (54, 2, [98, 87, 76, 65, 54, 43, 32, 21, 10]),

    (0, 3, [0]),
    (11, 3, [2, 11, 20]),
    (9, 3, [9, 18, 27, 36, 45]),
    (21, 3, [30, 21, 12, 3]),
    (31, 3, [40, 31, 22, 13, 4]),
    (88, 3, [79, 88, 97]),
    (54, 3, [18, 27, 36, 45, 54, 63, 72, 81, 90]),
    (93, 3, [93, 84, 75, 66, 57]),
    (68, 3, [59, 68, 77, 86, 95]),
    (5, 3, [5, 14, 23, 32, 41]),
])
def test_get_pos_for_direction(pos, direction, res):
    board = Board(10)
    node = Node(None, -1, {}, {}, {}, board.size)
    assert sorted(res) == node.get_pos_for_direction(pos, direction)


def test_score_pos_empty():
    """Map:
.........
.........
.........
.........
.........
.........
.........
.........
.........
    """
    board = Board(10)
    board.play(board.coord_to_action(4, 4), Color.black)
    state = GomokuState(board, Color.black)
    node = Node(None, -1, state.empty, state.mine, state.others, board.size)
    exp_score = 5 * 4 * 3
    assert exp_score == node.score_pos(board.coord_to_action(4, 4))


def test_score_pos_0():
    """Map:
.........
.........
.........
.........
....X....
.........
.........
.........
.........
    """
    board = Board(9)
    board = board.play(board.coord_to_action(4, 4), Color.black)
    state = GomokuState(board, Color.black)
    node = Node(None, -1, state.empty, state.mine, state.others, board.size)
    total_rows = 5 * 4
    exp_score = total_rows * 7
    assert exp_score == node.score_pos(board.coord_to_action(4, 4))


def test_score_pos_1():
    """Map:
.........
.........
.........
.........
....XX...
.........
.........
.........
.........
    """
    board = Board(9)
    board = board.play(board.coord_to_action(4, 4), Color.black)
    board = board.play(board.coord_to_action(4, 5), Color.black)
    state = GomokuState(board, Color.black)
    node = Node(None, -1, state.empty, state.mine, state.others, board.size)
    total_rows = 5 * 4
    exp_score = (total_rows - 4) * 7 + 4 * 11
    assert exp_score == node.score_pos(board.coord_to_action(4, 4))


def test_score_board():
    board = Board(9)
    board = board.play(board.coord_to_action(4, 3), Color.black)
    board = board.play(board.coord_to_action(4, 4), Color.black)
    state = GomokuState(board, Color.black)
    node1 = Node(None, -1, state.empty, state.mine, state.others, board.size)

    board = board.play(board.coord_to_action(4, 6), Color.black)
    state = GomokuState(board, Color.black)
    node2 = Node(None, -1, state.empty, state.mine, state.others, board.size)

    board = board.play(board.coord_to_action(4, 5), Color.black)
    state = GomokuState(board, Color.black)
    node3 = Node(None, -1, state.empty, state.mine, state.others, board.size)

    assert node1.score_board() < node2.score_board() < node3.score_board()

