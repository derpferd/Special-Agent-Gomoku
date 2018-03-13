# Author: Vaclav Hasenohrl
from collections import namedtuple
from random import choice
from typing import List
from math import sqrt, pow
from copy import deepcopy

from utils import Verbosity
from .. import Agent
from gym_gomoku import GomokuState


Threat = namedtuple('Threat', ['positions', 'stones'])


class Node:
    WINNING_SCORE = 20000
    BLOCK_WIN_SCORE = 200000

    def __init__(self, parent, pos, free, player, opponent):
        self.parent = parent
        self.pos = pos
        if pos != -1:
            self.f = free - {pos}
            self.p = player | {pos}
            self.o = opponent.copy()
        else:
            self.f = free.copy()
            self.p = player.copy()
            self.o = opponent.copy()
        self.reward = 0
        self.attacks = {}  # A mapping of prospective moves to their score.
        # self.threats = {}  # A mapping of threats to their scores.
        # self.attacks = {}  # A mapping of threats to their scores.

    # returns the number of (rows/columns)^2 - 1
    def get_board_size(self):
        return len(self.f) + len(self.p) + len(self.o)

    def is_in(self, threat, s):
        for t in s:
            if t[0] == threat:
                return True

        return False

    def get_rewards(self, threat, turn):
        """

        Args:
            threat(Threat): A threat given a opp's stone.
            turn:

        Returns:

        """
        score = 0
        if turn == 0:
            if not self.is_in(threat[0], self.attacks):
                if threat[1] == 3 and len(threat[0]) == 5:
                    score = 1000
                elif threat[1] == 4 and len(threat[0]) == 5:
                    score = self.WINNING_SCORE
                elif threat[1] == 4 and len(threat[0]) == 6:
                    score = self.WINNING_SCORE
                elif threat[1] == 1 and len(threat[0]) == 3:
                    score = 1
                elif threat[1] == 2 and len(threat[0]) == 4:
                    score = 10
                elif threat[1] == 5:
                    score = self.WINNING_SCORE
        else:
            if not self.is_in(sorted(threat[0]), self.attacks):
                if threat[1] == 3 and len(threat[0]) == 5:
                    score = -999
                elif threat[1] == 4 and len(threat[0]) == 5:
                    score = -self.BLOCK_WIN_SCORE
                elif threat[1] == 4 and len(threat[0]) == 6:
                    score = -self.BLOCK_WIN_SCORE
                elif threat[1] == 5:
                    score = -self.BLOCK_WIN_SCORE
        if score:
            self.attacks[threat] = score
            self.reward = sum(self.attacks.values())

    def check_rows(self, curr, turn):
        row_length = int(sqrt(self.get_board_size() + 1))
        s = self.p if turn == 0 else self.o
        threat = [curr]
        # check rows
        # left
        count = 1
        moves = 1
        while (curr - moves) // row_length == curr // row_length:
            if curr - moves in s:
                threat.append(curr - moves)
                moves += 1
                count += 1
            elif curr - moves in self.f:
                threat.append(curr - moves)
                break
            else:
                break
        # right
        moves = 1
        while (curr + moves) // row_length == curr // row_length:
            if curr + moves in s:
                threat.append(curr + moves)
                moves += 1
                count += 1
            elif curr + moves in self.f:
                threat.append(curr + moves)
                break
            else:
                break

        threat = sorted(threat) if turn == 1 else threat
        threat = Threat(tuple(threat), count)
        self.get_rewards(threat, turn)

    def check_columns(self, curr, turn):
        row_length = int(sqrt(self.get_board_size() + 1))
        s = self.p if turn == 0 else self.o
        threat = [curr]
        # check columns
        # down
        count = 1
        moves = 1
        while curr - moves * row_length >= 0:
            if curr - moves * row_length in s:
                threat.append(curr - moves * row_length)
                moves += 1
                count += 1
            elif curr - moves * row_length in self.f:
                threat.append(curr - moves * row_length)
                break
            else:
                break
        # up
        moves = 1
        while curr + moves * row_length < pow(row_length, 2):
            if curr + moves * row_length in s:
                threat.append(curr + moves * row_length)
                moves += 1
                count += 1
            elif curr + moves * row_length in self.f:
                threat.append(curr + moves * row_length)
                break
            else:
                break

        threat = sorted(threat) if turn == 1 else threat
        threat = Threat(tuple(threat), count)
        self.get_rewards(threat, turn)

    def check_diag(self, curr, turn):
        row_length = int(sqrt(self.get_board_size() + 1))
        s = self.p if turn == 0 else self.o
        threat = [curr]
        r = curr // row_length
        c = curr - r * row_length
        # check left to right
        # down
        count = 1
        moves = 1
        while r - moves >= 0 and c + moves < row_length:
            if (r - moves) * row_length + (c + moves) in s:
                threat.append((r - moves) * row_length + (c + moves))
                moves += 1
                count += 1
            elif (r - moves) * row_length + (c + moves) in self.f:
                threat.append((r - moves) * row_length + (c + moves))
                break
            else:
                break
        # up
        moves = 1
        while r + moves < row_length and c - moves >= 0:
            if (r + moves) * row_length + (c - moves) in s:
                threat.append((r + moves) * row_length + (c - moves))
                moves += 1
                count += 1
            elif (r + moves) * row_length + (c - moves) in self.f:
                threat.append((r + moves) * row_length + (c - moves))
                break
            else:
                break

        threat = sorted(threat) if turn == 1 else threat
        threat = Threat(tuple(threat), count)
        self.get_rewards(threat, turn)

        threat = [curr]
        # check right to left
        # down
        count = 1
        moves = 1
        while r - moves >= 0 and c - moves >= 0:
            if (r - moves) * row_length + (c - moves) in s:
                threat.append((r - moves) * row_length + (c - moves))
                moves += 1
                count += 1
            elif (r - moves) * row_length + (c - moves) in self.f:
                threat.append((r - moves) * row_length + (c - moves))
                break
            else:
                break
        # up
        moves = 1
        while r + moves < row_length and c + moves < row_length:
            if (r + moves) * row_length + (c + moves) in s:
                threat.append((r + moves) * row_length + (c + moves))
                moves += 1
                count += 1
            elif (r + moves) * row_length + (c + moves) in self.f:
                threat.append((r + moves) * row_length + (c + moves))
                break
            else:
                break

        threat = sorted(threat) if turn == 1 else threat
        threat = Threat(tuple(threat), count)
        self.get_rewards(threat, turn)

    def analyze_opponent(self):
        stack = self.o.copy()
        while stack:
            curr = stack.pop()
            self.check_rows(curr, 1)
            self.check_columns(curr, 1)
            self.check_diag(curr, 1)

    def analyze_players_move(self, curr):
        self.check_rows(curr, 0)
        self.check_columns(curr, 0)
        self.check_diag(curr, 0)


class ABP(Agent):
    def find_optimal_move(self, leaves: List[Node]):
        if self.config.verbose.at_level(Verbosity.debug):
            for leave in leaves:
                print("Leave score is: {} => {}".format(leave.pos, leave.reward))

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
        root = Node(None, -1, free, player, opponent)
        root.analyze_opponent()

        leaves = []
        for x in free:
            temp = Node(root, x, free, player, opponent)
            for t in temp.parent.attacks:
                new_threat = deepcopy(t)
                if x not in new_threat[0]:
                    temp.get_rewards(new_threat, 1)
            temp.analyze_players_move(x)
            leaves.append(temp)

        return self.find_optimal_move(leaves)
