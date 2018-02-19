# Author: Vaclav Hasenohrl
from random import choice
from typing import List
from math import sqrt

from .. import Agent
from gym_gomoku import GomokuState


class Node:
    def __init__(self, parent, pos, free, player, opponent):
        self.par = parent
        self.pos = pos
        if pos != -1:
            self.f = free ^ pos
            self.p = player.append(pos)
            self.o = opponent
        self.reward = parent.reward  # reward
        self.danger = 0  # danger
        self.threats = {}
        self.attacks = {}
        self.plays = {}

    # returns the number of (rows/columns)^2 - 1
    def get_board_size(self):
        return max(max(self.p, self.o), self.f)

    def get_rewards(self, threat, count, turn):
        if turn == 0:
            if threat not in self.attacks:
                if count == 3 and len(threat) == 5:
                    self.attacks.append((threat, 1000))
                    self.danger += 1000
                elif count == 4 and len(threat) == 5:
                    self.attacks.append((threat, 20000))
                    self.danger += 20000
                elif count == 4 and len(threat) == 6:
                    self.attacks.append((threat, 20000))
                    self.danger += 20000
            if threat not in self.plays:
                if count == 1 and len(threat) == 3:
                    self.plays.append((threat, 1))
                    self.reward += 1
                elif count == 2 and len(threat) == 4:
                    self.plays.append((threat, 5))
                    self.reward += 5
        else:
            if threat not in self.threats:
                if count == 3 and len(threat) == 5:
                    self.threats.append((threat, -1000))
                    self.danger += -1000
                elif count == 4 and len(threat) == 5:
                    self.threats.append((threat, -20000))
                    self.danger += -20000
                elif count == 4 and len(threat) == 6:
                    self.threats.append((threat, -20000))
                    self.danger += -20000

    def check_rows(self, curr, turn):
        row_length = sqrt(self.get_board_size() + 1)
        threat = {(curr, 0)}
        # check rows
        # left
        count = 1
        moves = 1
        while (curr - moves) % row_length == curr % row_length:
            if curr - moves in self.o:
                threat.append((curr - moves, 0))
                moves += 1
                count += 1
            elif curr - moves in self.f:
                threat.append((curr - moves, 1))
                break
            else:
                break
        # right
        moves = 1
        while (curr + moves) % row_length == curr % row_length:
            if curr + moves in self.o:
                threat.append((curr - moves, 0))
                moves += 1
                count += 1
            elif curr + moves in self.f:
                threat.append((curr - moves, 1))
                break
            else:
                break

        self.get_rewards(threat, count, turn)

    def check_columns(self, curr, turn):
        row_length = sqrt(self.get_board_size() + 1)
        threat = {(curr, 0)}
        # check columns
        # down
        count = 1
        moves = 1
        while curr - moves * row_length >= 0:
            if curr - moves * row_length in self.o:
                threat.append((curr - moves * row_length, 0))
                moves += 1
                count += 1
            elif curr - moves * row_length in self.f:
                threat.append((curr - moves * row_length, 1))
                break
            else:
                break
        # up
        moves = 1
        while curr + moves * row_length < row_length ^ 2:
            if curr + moves * row_length in self.o:
                threat.append((curr - moves * row_length, 0))
                moves += 1
                count += 1
            elif curr + moves * row_length in self.f:
                threat.append((curr - moves * row_length, 1))
                break
            else:
                break

        self.get_rewards(threat, count, turn)

    def check_diag(self, curr, turn):
        row_length = sqrt(self.get_board_size() + 1)
        threat = {(curr, 0)}
        r = curr % row_length
        c = curr - r * row_length
        # check left to right
        # down
        count = 1
        moves = 1
        while r - moves >= 0 and c + moves < row_length:
            if (r - moves) * row_length + (c + moves) in self.o:
                threat.append(((r - moves) * row_length + (c + moves), 0))
                moves += 1
                count += 1
            elif (r - moves) * row_length + (c + moves) in self.f:
                threat.append(((r - moves) * row_length + (c + moves), 1))
                break
            else:
                break
        # up
        moves = 1
        while r + moves < row_length and c - moves >= 0:
            if (r + moves) * row_length + (c - moves) in self.o:
                threat.append(((r + moves) * row_length + (c - moves), 0))
                moves += 1
                count += 1
            elif (r + moves) * row_length + (c - moves) in self.f:
                threat.append(((r + moves) * row_length + (c - moves), 1))
                break
            else:
                break

        self.get_rewards(threat, count, turn)

        threat = {(curr, 0)}
        # check right to left
        # down
        count = 1
        moves = 1
        while r - moves >= 0 and c - moves >= 0:
            if (r - moves) * row_length + (c - moves) in self.o:
                threat.append(((r - moves) * row_length + (c - moves), 0))
                moves += 1
                count += 1
            elif (r - moves) * row_length + (c - moves) in self.f:
                threat.append(((r - moves) * row_length + (c - moves), 1))
                break
            else:
                break
        # up
        moves = 1
        while r + moves < row_length and c + moves < row_length:
            if (r + moves) * row_length + (c + moves) in self.o:
                threat.append(((r + moves) * row_length + (c + moves), 0))
                moves += 1
                count += 1
            elif (r + moves) * row_length + (c + moves) in self.f:
                threat.append(((r + moves) * row_length + (c + moves), 1))
                break
            else:
                break

        self.get_rewards(threat, count, turn)

    def analyze_opponent(self):
        stack = self.o[:]
        while stack:
            curr = stack.pop()
            self.check_rows(curr, 1)
            self.check_columns(curr, 1)
            self.check_diag(curr, 1)

    def analyze_player(self):
        stack = self.p[:]
        while stack:
            curr = stack.pop()
            self.check_rows(curr, 0)
            self.check_columns(curr, 0)
            self.check_diag(curr, 0)


class ABP(Agent):
    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        root = Node(None, -1, None, None, None)
        root.analyze_opponent()
        root.analyze_player()
        if root.danger >= 0 and root.attacks:
            index = 0
            m = -999999999
            for x in range(root.attacks):
                if root.attacks[x][1] > m:
                    m = root.attacks[x][1]
                    index = x
            # play the following
            root.attacks[index][0][len(root.attacks[index][0] - 1)]
        elif root.danger < 0
            index = 0
            m = 999999999
            for x in range(root.threats):
                if root.threats[x][1] < m:
                    m = root.attacks[x][1]
                    index = x
            # play the following
            root.threats[index][0][len(root.threats[index][0] - 1)]
        else:
            leaves = {}
            for x in free:
                temp = Node(root, x, free, player, opponent)
                temp.analyze_player()
                leaves.append(temp)
            # find the best Node
            index = 0
            m = -999999999
            for x in range(leaves):
                if leaves[x].reward > m:
                    m = leaves[x].reward
                    index = x
            # find what action to take
            index2 = 0
            m = -999999999
            for x in range(leaves[index].plays):
                if leaves[index].plays[x][1] < m:
                    m = leaves[index].plays[x][1]
                    index2 = x
            # play the following
            leaves[index].plays[index2][0][len(root.threats[index][0] - 1)]


        return choice(list(state.board.valid_actions))
