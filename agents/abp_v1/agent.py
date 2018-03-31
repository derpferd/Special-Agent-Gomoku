# Author: Vaclav Hasenohrl
# Jon is not helping :-P
from collections import namedtuple
from enum import IntEnum, unique
from random import choice
from typing import List
from math import sqrt, pow
from copy import deepcopy

from utils import Verbosity
from .. import Agent
from gym_gomoku import GomokuState


Combination = namedtuple('Combination', ['positions', 'reward'])
Attack = namedtuple('Attack', ['positions', 'count'])


@unique
class Direction(IntEnum):
    horizontal = 0
    vertical = 1
    diagonal_l_to_r = 2
    diagonal_r_to_l = 3


class Node:
    WINNING_SCORE = 20000
    BLOCK_WIN_SCORE = 200000
    COMBINATIONS = []

    # 1 stone combinations
    COMBINATIONS.append(Combination(tuple([0, 0, 1, 0, 0]), 1))

    # 2 stone combinations
    COMBINATIONS.append(Combination(tuple([0, 0, 1, 1, 0]), 5))
    COMBINATIONS.append(Combination(tuple([0, 1, 1, 0, 0]), 5))
    COMBINATIONS.append(Combination(tuple([0, 0, 1, 0, 1]), 5))
    COMBINATIONS.append(Combination(tuple([1, 0, 1, 0, 0]), 5))
    COMBINATIONS.append(Combination(tuple([0, 1, 0, 1, 0]), 5))

    # 3 stone combinations
    COMBINATIONS.append(Combination(tuple([1, 1, 1, 0, 0]), 70))
    COMBINATIONS.append(Combination(tuple([0, 0, 1, 1, 1]), 70))
    COMBINATIONS.append(Combination(tuple([0, 1, 1, 1, 0]), 70))
    COMBINATIONS.append(Combination(tuple([0, 1, 1, 1, 0]), 70))
    COMBINATIONS.append(Combination(tuple([0, 1, 1, 0, 1]), 70))
    COMBINATIONS.append(Combination(tuple([1, 0, 1, 1, 0]), 70))
    COMBINATIONS.append(Combination(tuple([1, 0, 1, 0, 1]), 70))

    # 4 stone combinations
    COMBINATIONS.append(Combination(tuple([0, 1, 1, 1, 1]), 800))
    COMBINATIONS.append(Combination(tuple([1, 0, 1, 1, 1]), 800))
    COMBINATIONS.append(Combination(tuple([1, 1, 0, 1, 1]), 800))
    COMBINATIONS.append(Combination(tuple([1, 1, 1, 1, 0]), 800))
    # 5 stone combinations (losing pattern)
    COMBINATIONS.append(Combination(tuple([1, 1, 1, 0, 1]), 800))

    COMBINATIONS.append(Combination(tuple([1, 1, 1, 1, 1]), 6000))

    def __init__(self, parent, pos, free, player, opponent, board_size):
        self.parent = parent
        self.pos = pos
        if pos != -1:
            self.f = free - {pos}
            self.p = player | {pos}
            self.o = opponent.copy()
            self.combinations = parent.combinations.copy()  # A mapping of prospective moves to their score
            self.reward = parent.reward
        else:
            self.f = free.copy()
            self.p = player.copy()
            self.o = opponent.copy()
            self.combinations = {}  # A mapping of prospective moves to their score
            self.reward = 0
        self.board_size = board_size

    # OLD CODE

    # def get_rewards(self, threat, turn):
    #     """
    #
    #     Args:
    #         threat(Threat): A threat given a opp's stone.
    #         turn:
    #
    #     Returns:
    #
    #     """
    #     score = 0
    #     if turn == 0:
    #         if not self.is_in(threat[0], self.attacks):
    #             if threat[1] == 3 and len(threat[0]) == 5:
    #                 score = 900
    #             elif threat[1] == 4 and len(threat[0]) == 5:
    #                 score = self.WINNING_SCORE
    #             elif threat[1] == 4 and len(threat[0]) == 6:
    #                 score = self.WINNING_SCORE
    #             elif threat[1] == 1 and len(threat[0]) == 3:
    #                 score = 1
    #             elif threat[1] == 2 and len(threat[0]) == 4:
    #                 score = 9
    #             elif threat[1] == 5:
    #                 score = self.WINNING_SCORE
    #     else:
    #         if not self.is_in(sorted(threat[0]), self.attacks):
    #             if threat[1] == 3 and len(threat[0]) == 5:
    #                 score = -999
    #             elif threat[1] == 4 and len(threat[0]) == 5:
    #                 score = -self.BLOCK_WIN_SCORE
    #             elif threat[1] == 4 and len(threat[0]) == 6:
    #                 score = -self.BLOCK_WIN_SCORE
    #             elif threat[1] == 5:
    #                 score = -self.BLOCK_WIN_SCORE
    #     if score:
    #         self.attacks[threat] = score
    #         self.reward = sum(self.attacks.values())

    # def check_rows(self, curr, turn):
    #     row_length = int(sqrt(self.get_board_size() + 1))
    #     s = self.p if turn == 0 else self.o
    #     threat = [curr]
    #     # check rows
    #     # left
    #     count = 1
    #     moves = 1
    #     while (curr - moves) // row_length == curr // row_length:
    #         if curr - moves in s:
    #             threat.append(curr - moves)
    #             moves += 1
    #             count += 1
    #         elif curr - moves in self.f:
    #             threat.append(curr - moves)
    #             break
    #         else:
    #             break
    #     # right
    #     moves = 1
    #     while (curr + moves) // row_length == curr // row_length:
    #         if curr + moves in s:
    #             threat.append(curr + moves)
    #             moves += 1
    #             count += 1
    #         elif curr + moves in self.f:
    #             threat.append(curr + moves)
    #             break
    #         else:
    #             break
    #
    #     threat = sorted(threat) if turn == 1 else threat
    #     threat = Attack(tuple(threat), count)
    #     self.get_rewards(threat, turn)
    #
    # def check_columns(self, curr, turn):
    #     row_length = int(sqrt(self.get_board_size() + 1))
    #     s = self.p if turn == 0 else self.o
    #     threat = [curr]
    #     # check columns
    #     # down
    #     count = 1
    #     moves = 1
    #     while curr - moves * row_length >= 0:
    #         if curr - moves * row_length in s:
    #             threat.append(curr - moves * row_length)
    #             moves += 1
    #             count += 1
    #         elif curr - moves * row_length in self.f:
    #             threat.append(curr - moves * row_length)
    #             break
    #         else:
    #             break
    #     # up
    #     moves = 1
    #     while curr + moves * row_length < pow(row_length, 2):
    #         if curr + moves * row_length in s:
    #             threat.append(curr + moves * row_length)
    #             moves += 1
    #             count += 1
    #         elif curr + moves * row_length in self.f:
    #             threat.append(curr + moves * row_length)
    #             break
    #         else:
    #             break
    #
    #     threat = sorted(threat) if turn == 1 else threat
    #     threat = Attack(tuple(threat), count)
    #     self.get_rewards(threat, turn)
    #
    # def check_diag(self, curr, turn):
    #     row_length = int(sqrt(self.get_board_size() + 1))
    #     s = self.p if turn == 0 else self.o
    #     threat = [curr]
    #     r = curr // row_length
    #     c = curr - r * row_length
    #     # check left to right
    #     # down
    #     count = 1
    #     moves = 1
    #     while r - moves >= 0 and c + moves < row_length:
    #         if (r - moves) * row_length + (c + moves) in s:
    #             threat.append((r - moves) * row_length + (c + moves))
    #             moves += 1
    #             count += 1
    #         elif (r - moves) * row_length + (c + moves) in self.f:
    #             threat.append((r - moves) * row_length + (c + moves))
    #             break
    #         else:
    #             break
    #     # up
    #     moves = 1
    #     while r + moves < row_length and c - moves >= 0:
    #         if (r + moves) * row_length + (c - moves) in s:
    #             threat.append((r + moves) * row_length + (c - moves))
    #             moves += 1
    #             count += 1
    #         elif (r + moves) * row_length + (c - moves) in self.f:
    #             threat.append((r + moves) * row_length + (c - moves))
    #             break
    #         else:
    #             break
    #
    #     threat = sorted(threat) if turn == 1 else threat
    #     threat = Attack(tuple(threat), count)
    #     self.get_rewards(threat, turn)
    #
    #     threat = [curr]
    #     # check right to left
    #     # down
    #     count = 1
    #     moves = 1
    #     while r - moves >= 0 and c - moves >= 0:
    #         if (r - moves) * row_length + (c - moves) in s:
    #             threat.append((r - moves) * row_length + (c - moves))
    #             moves += 1
    #             count += 1
    #         elif (r - moves) * row_length + (c - moves) in self.f:
    #             threat.append((r - moves) * row_length + (c - moves))
    #             break
    #         else:
    #             break
    #     # up
    #     moves = 1
    #     while r + moves < row_length and c + moves < row_length:
    #         if (r + moves) * row_length + (c + moves) in s:
    #             threat.append((r + moves) * row_length + (c + moves))
    #             moves += 1
    #             count += 1
    #         elif (r + moves) * row_length + (c + moves) in self.f:
    #             threat.append((r + moves) * row_length + (c + moves))
    #             break
    #         else:
    #             break
    #
    #     threat = sorted(threat) if turn == 1 else threat
    #     threat = Attack(tuple(threat), count)
    #     self.get_rewards(threat, turn)

    def check_rows(self, curr, turn):
        row_length = self.board_size
        s = self.p if turn == 0 else self.o
        r = curr // row_length
        c = curr - r * row_length
        threat = []

        # check rows
        # left
        moves = 1
        for i in range(2):
            if c - moves < 0:
                break
            if curr - moves in s:
                threat.append((curr - moves) + 1000)
            elif curr - moves in self.f:
                threat.append((curr - moves) + 0)
            else:
                break
            moves += 1
        # right
        threat.append(curr + 1000)
        moves = 1
        for i in range(2):
            if c + moves >= row_length:
                break
            if curr + moves in s:
                threat.append((curr + moves) + 1000)
            elif curr + moves in self.f:
                threat.append((curr + moves) + 0)
            else:
                break
            moves += 1
        self.evaluate_pattern(threat, turn)

    def check_columns(self, curr, turn):
        row_length = self.board_size
        s = self.p if turn == 0 else self.o
        r = curr // row_length
        c = curr - r * row_length
        threat = []

        # check columns
        # down
        moves = 1
        for i in range(2):
            if r - moves < 0:
                break
            if curr - moves * row_length in s:
                threat.append((curr - moves * row_length) + 1000)
            elif curr - moves * row_length in self.f:
                threat.append((curr - moves * row_length) + 0)
            else:
                break
            moves += 1
        # up
        threat.append(curr + 1000)
        moves = 1
        for i in range(2):
            if r + moves >= row_length:
                break
            if curr + moves * row_length in s:
                threat.append((curr + moves * row_length) + 1000)
            elif curr + moves * row_length in self.f:
                threat.append((curr + moves * row_length) + 0)
            else:
                break
            moves += 1
        self.evaluate_pattern(threat, turn)

    def check_diag(self, curr, turn):
        row_length = self.board_size
        s = self.p if turn == 0 else self.o
        r = curr // row_length
        c = curr - r * row_length
        threat = []

        # right/down
        moves = 1
        for i in range(2):
            if r - moves < 0 or c + moves >= row_length:
                break
            if curr - moves * row_length + moves in s:
                threat.append((curr - moves * row_length + moves) + 1000)
            elif curr - moves * row_length + moves in self.f:
                threat.append((curr - moves * row_length + moves) + 0)
            else:
                break
            moves += 1
        # left/up
        threat.append(curr + 1000)
        moves = 1
        for i in range(2):
            if r + moves >= row_length or c - moves < 0:
                break
            if curr + moves * row_length - moves in s:
                threat.append((curr + moves * row_length - moves) + 1000)
            elif curr + moves * row_length - moves in self.f:
                threat.append((curr + moves * row_length - moves) + 0)
            else:
                break
            moves += 1
        self.evaluate_pattern(threat, turn)

        # left/down
        threat = []
        moves = 1
        for i in range(2):
            if r - moves < 0 or c - moves < 0:
                break
            if curr - moves * row_length - moves in s:
                threat.append((curr - moves * row_length - moves) + 1000)
            elif curr - moves * row_length - moves in self.f:
                threat.append((curr - moves * row_length - moves) + 0)
            else:
                break
            moves += 1
        # right/up
        threat.append(curr + 1000)
        moves = 1
        for i in range(2):
            if r + moves >= row_length or c + moves >= row_length:
                break
            if curr + moves * row_length + moves in s:
                threat.append((curr + moves * row_length + moves) + 1000)
            elif curr + moves * row_length + moves in self.f:
                threat.append((curr + moves * row_length + moves) + 0)
            else:
                break
            moves += 1
        self.evaluate_pattern(threat, turn)

    def evaluate_pattern(self, threat, turn):
        if len(threat) != 5:
            return
        temp_threat = []
        for i in range(len(threat)):
            temp_threat.append(threat[i] // 1000)
        for t in self.COMBINATIONS:
            if temp_threat == list(t[0]):
                score = t[1] if turn % 2 == 0 else -5 * t[1]
                if tuple(sorted(threat)) not in self.combinations:
                    self.combinations[tuple(sorted(threat))] = score
                    self.reward += score
        return

    def analyze_board_root(self):
        stack = self.o.copy()
        while stack:
            curr = stack.pop()
            self.check_rows(curr, 1)
            self.check_columns(curr, 1)
            self.check_diag(curr, 1)

    def analyze_player(self, curr, turn):
        stack = self.p.copy()
        stack.add(curr)
        while stack:
            curr = stack.pop()
            self.check_rows(curr, turn)
            self.check_columns(curr, turn)
            self.check_diag(curr, turn)

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
            return list(map(lambda i: (i * self.board_size) + i + pos, range(max(-4, d_x_0, d_y_0), min(5, d_x_m, d_y_m))))
        elif direction == Direction.diagonal_r_to_l:
            return list(map(lambda i: -(i * self.board_size) + pos + i, reversed(range(max(-4, d_x_0, -(d_y_m-1)), min(5, d_x_m, y+1)))))

    SCORES = {i: v for i, v in enumerate((0, 19, 15, 11, 7, 3))}

    def score_pos(self, pos):
        score = 0
        for direction in Direction:
            for row in zip(*[self.get_pos_for_direction(pos, direction)[i:] for i in range(5)]):
                empty_spaces = sum(map(lambda x: 0 if x in self.p else 1 if x in self.f else 100, row))
                score += self.SCORES.get(empty_spaces, 0)
        return score

    def score_board(self):
        return sum(self.score_pos(i) for i in range(self.board_size**2))


class ABP(Agent):
    def check_free_positions_radius_n(self, curr, free, n):
        row_length = 19
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

    def append_free_positions_radius_n(self, free, player, opponent, n):
        free_mod = set()
        p = player.copy()
        o = opponent.copy()
        while p:
            curr = p.pop()
            free_mod = free_mod | self.check_free_positions_radius_n(curr, free, n)
        while o:
            curr = o.pop()
            free_mod = free_mod | self.check_free_positions_radius_n(curr, free, n)
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
        if len(free) == 361:
            return 180

        free_pruned = self.append_free_positions_radius_n(free, player, opponent, 2)
        root = Node(None, -1, free, player, opponent, state.board.size)
        root.analyze_board_root()

        turn = 0
        parents = [root]
        leaves = []
        for i in range(1):
            for node in parents:
                for x in free_pruned:
                    temp = Node(node, x, free, player, opponent, state.board.size)
                    for t in temp.parent.combinations:
                        if x in t:
                            temp.reward -= temp.combinations[t]
                            del temp.combinations[t]
                    temp.analyze_player(x, turn % 2)
                    leaves.append(temp)
            if turn % 2 == 0:
                parents = sorted(leaves, key=lambda x: x.reward)[-len(leaves) // 5:]
                if not parents:
                    parents = [sorted(leaves, key=lambda x: x.reward)[-1]]
            else:
                parents = sorted(leaves, key=lambda x: x.reward)[:len(leaves) // 5]
                if not parents:
                    parents = [sorted(leaves, key=lambda x: x.reward)[0]]
            turn = turn + 1
            leaves = []

        move = self.find_optimal_move(parents)
        return move
