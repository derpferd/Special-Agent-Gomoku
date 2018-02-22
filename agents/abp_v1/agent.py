# Author: Vaclav Hasenohrl
from random import choice
from typing import List
from math import sqrt, pow
from copy import deepcopy

from .. import Agent
from gym_gomoku import GomokuState


class Node:
    def __init__(self, parent, pos, free, player, opponent):
        self.parent = parent
        self.pos = pos
        if pos != -1:
            self.f = free - {pos}
            temp = player.copy()
            temp.add(pos)
            self.p = temp.copy()
            self.o = opponent
        else:
            self.f = free
            self.p = player
            self.o = opponent
        self.reward = 0
        self.threats = []
        self.attacks = []

    # returns the number of (rows/columns)^2 - 1
    def get_board_size(self):
        return len(self.f) + len(self.p) + len(self.o)

    def is_in(self, threat, s):
        for t in s:
            if t[0] == threat:
                return True

        return False

    def get_rewards(self, threat, turn):
        if turn == 0:
            if not self.is_in(threat[0], self.attacks):
                if threat[1][0] == 3 and len(threat[0]) == 5:
                    threat[1][1] = 1000
                    self.attacks.append(threat)
                    self.reward += 1000
                elif threat[1][0] == 4 and len(threat[0]) == 5:
                    threat[1][1] = 20000
                    self.attacks.append(threat)
                    self.reward += 20000
                elif threat[1][0] == 4 and len(threat[0]) == 6:
                    threat[1][1] = 20000
                    self.attacks.append(threat)
                    self.reward += 20000
                elif threat[1][0] == 1 and len(threat[0]) == 3:
                    threat[1][1] = 1
                    self.attacks.append(threat)
                    self.reward += 1
                elif threat[1][0] == 2 and len(threat[0]) == 4:
                    threat[1][1] = 5
                    self.attacks.append(threat)
                    self.reward += 5
                elif threat[1][0] == 5:
                    threat[1][1] = 1000000
                    self.attacks.append(threat)
                    self.reward += 1000000
        else:
            if not self.is_in(sorted(threat[0]), self.threats):
                if threat[1][0] == 3 and len(threat[0]) == 5:
                    threat[1][1] = -10000
                    self.threats.append(threat)
                    self.reward -= 10000
                elif threat[1][0] == 4 and len(threat[0]) == 5:
                    threat[1][1] = -200000
                    self.threats.append(threat)
                    self.reward -= 200000
                elif threat[1][0] == 4 and len(threat[0]) == 6:
                    threat[1][1] = -200000
                    self.threats.append(threat)
                    self.reward -= 200000
                elif threat[1][0] == 5:
                    threat[1][1] = -10000000
                    self.threats.append(threat)
                    self.reward -= 10000000

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
        threat = (threat, [count, 0])
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
        threat = (threat, [count, 0])
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
        threat = (threat, [count, 0])
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
        threat = (threat, [count, 0])
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
    def find_optimal_move(self, leaves):
        # find the best Node
        index = 0
        m = float('-inf')
        for x in range(len(leaves)):
            if leaves[x].reward > m:
                m = leaves[x].reward
                index = x

        return leaves[index].pos

    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        free = state.empty.copy()
        player = state.mine.copy()
        opponent = state.others.copy()
        root = Node(None, -1, free, player, opponent)
        root.analyze_opponent()

        leaves = []
        for x in free:
            temp = Node(root, x, free, player, opponent)
            for t in temp.parent.threats:
                new_threat = deepcopy(t)
                if x in new_threat[0]:
                    new_threat[0].remove(x)
                temp.get_rewards(new_threat, 1)
            temp.analyze_players_move(x)
            leaves.append(temp)

        return self.find_optimal_move(leaves)





