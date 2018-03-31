# Author: Jon and Vaclav didn't do anything... :)
from collections import namedtuple
from enum import IntEnum, unique
from typing import List

from gym_gomoku import GomokuState

from .. import Agent

Pattern = namedtuple('Pattern', ['positions', 'reward'])


def cached(func):
    MEMO = {}
    def wrapped(*args):
        if args not in MEMO:
            v = func(*args)
            MEMO[args] = v
        return MEMO[args]
    return wrapped


@unique
class Direction(IntEnum):
    horizontal = 0
    vertical = 1
    diagonal_l_to_r = 2
    diagonal_r_to_l = 3


class Node:
    WINNING_SCORE = 20000
    BLOCK_WIN_SCORE = 200000

    def __init__(self, parent, pos, free, player, opponent, board_size, turn):
        self.parent = parent  # Type: Node
        self.pos = pos
        self.board_size = board_size
        self.turn = turn
        if pos != -1:
            self.f = free - {pos}
            self.p = player | {pos}
            self.o = opponent.copy()
            self.patterns = parent.patterns.copy()  # A mapping of prospective moves to their score
            self.reward = parent.reward
            self.update_reward()
            # Think about calling this:
            # temp.analyze_player(move, turn % 2)
        else:
            self.f = free.copy()
            self.p = player.copy()
            self.o = opponent.copy()
            # A mapping of prospective moves to their score
            self.patterns = {}  # type: Dict[tuple, int]
            self.reward = 0
            self.analyze_board_root()

    def update_reward(self):
        for pattern in self.parent.patterns:
            if self.pos in pattern:
                self.reward -= self.patterns[pattern]
                del self.patterns[pattern]
        score, rows = self.score_pos(self.pos, self.turn)
        self.patterns.update(rows)
        self.reward += score

    def analyze_board_root(self):
        for stone_pos in self.o:
            score, rows = self.score_pos(stone_pos, self.turn)
            self.patterns.update(rows)
            self.reward += score

    @cached
    def get_pos_for_direction(self, pos: int, direction: Direction) -> List[int]:
        """

        Args:
            pos: The center position
            direction: The direction to get the positions of.

        Returns:
            A sorted list of positions connected to the `pos` with in 4 spaces.
        """
        x, y = pos % self.board_size, pos // self.board_size
        d_x_0, d_x_m = 0 - x, self.board_size - x
        d_y_0, d_y_m = 0 - y, self.board_size - y

        if direction == Direction.horizontal:
            return list(map(lambda i: i + pos, range(max(-4, d_x_0), min(5, d_x_m))))
        elif direction == Direction.vertical:
            return list(map(lambda i: (i * self.board_size) + pos, range(max(-4, d_y_0), min(5, d_y_m))))
        elif direction == Direction.diagonal_l_to_r:
            return list(
                map(lambda i: (i * self.board_size) + i + pos, range(max(-4, d_x_0, d_y_0), min(5, d_x_m, d_y_m))))
        elif direction == Direction.diagonal_r_to_l:
            return list(map(lambda i: -(i * self.board_size) + pos + i,
                            reversed(range(max(-4, d_x_0, -(d_y_m - 1)), min(5, d_x_m, y + 1)))))

    # SCORES = {i: v for i, v in enumerate((0, 19, 15, 11, 7, 3))}
    SCORES = {i: v for i, v in enumerate((10000, 1000, 100, 10, 1))}

    def score_pos(self, pos, turn):
        s = self.o if turn else self.p
        score_factor = -5 if turn else 1
        score = 0
        rows = {}
        for direction in Direction:
            for row in zip(*[self.get_pos_for_direction(pos, direction)[i:] for i in range(5)]):
                empty_spaces = sum(map(lambda x: 0 if x in s else 1 if x in self.f else 100, row))
                row_score = self.SCORES.get(empty_spaces, 0)
                if row_score:
                    rows[row] = score_factor * row_score
                    score += rows[row]
        return score, rows

    def score_board(self):
        return sum(self.score_pos(i) for i in range(self.board_size ** 2))


class ABP(Agent):
    def check_free_positions_radius_n(self, board_size, curr, free, n):
        row_length = board_size
        r = curr // row_length
        c = curr - r * row_length
        moves = 1
        free_mod = set()

        for i in range(n):
            # left
            if c - moves >= 0 and curr - moves in free:
                free_mod.add(curr - moves)
            # right
            if c + moves < row_length and curr + moves in free:
                free_mod.add(curr + moves)
            # down
            if r - moves >= 0 and curr - moves * row_length in free:
                free_mod.add(curr - moves * row_length)
            # up
            if r + moves < row_length and curr + moves * row_length in free:
                free_mod.add(curr + moves * row_length)
            # left/down
            if r - moves >= 0 and c - moves >= 0 and curr - moves * row_length - moves in free:
                free_mod.add(curr - moves * row_length - moves)
            # right/down
            if r - moves >= 0 and c + moves < row_length and curr - moves * row_length + moves in free:
                free_mod.add(curr - moves * row_length + moves)
            # left/up
            if r + moves < row_length and c - moves >= 0 and curr + moves * row_length - moves in free:
                free_mod.add(curr + moves * row_length - moves)
            # right/up
            if r + moves < row_length and c + moves < row_length and curr + moves * row_length + moves in free:
                free_mod.add(curr + moves * row_length + moves)

        return free_mod

    def append_free_positions_radius_n(self, board_size, free, player, opponent, n):
        free_mod = set()
        p = player.copy()
        o = opponent.copy()
        while p:
            curr = p.pop()
            free_mod = free_mod | self.check_free_positions_radius_n(board_size, curr, free, n)
        while o:
            curr = o.pop()
            free_mod = free_mod | self.check_free_positions_radius_n(board_size, curr, free, n)
        return free_mod

    def find_optimal_move(self, leaves: List[Node]):
        # if self.config.verbose.at_level(Verbosity.debug):
        #     for leave in leaves:
        #         print("Leave score is: {} => {}".format(leave.pos, leave.reward))

        # find and return the best node pos
        return max(leaves, key=lambda x: x.reward).pos

    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        free = state.empty
        player = state.mine
        opponent = state.others
        if not len(player) + len(opponent):
            return (state.board.size ** 2) // 2

        free_pruned = self.append_free_positions_radius_n(state.board.size, free, player, opponent, 2)
        root = Node(None, -1, free, player, opponent, state.board.size, 1)
        root.analyze_board_root()

        turn = 0
        parents = [root]
        leaves = []
        for i in range(3):
            for node in parents:
                for move in free_pruned:
                    leaves += [Node(node, move, free, player, opponent, state.board.size, turn % 2)]
            if turn % 2 == 0:
                parents = sorted(leaves, key=lambda x: x.reward)[-len(leaves) // 10:]
                if not parents:
                    parents = [sorted(leaves, key=lambda x: x.reward)[-1]]
            else:
                parents = sorted(leaves, key=lambda x: x.reward)[:len(leaves) // 10]
                if not parents:
                    parents = [sorted(leaves, key=lambda x: x.reward)[0]]
            turn = turn + 1
            leaves = []

        move = self.find_optimal_move(parents)
        return move
