# Author: Vaclav Hasenohrl
from random import choice
from typing import List
from math import sqrt

from .. import Agent
from gym_gomoku import GomokuState


class Node:
    def __init__(self, parent, free, player, opponent, move):
        self.par = parent
        self.f = free
        self.p = player
        self.o = opponent
        self.m = move  # whose move it is
        self.r = 0  # reward
        self.threats = {}

    # returns the number of (rows/columns)^2 - 1
    def get_board_size(self):
        return max(max(self.p, self.o), self.f)

    def check_rows(self, curr, stack):
        row_length = sqrt(self.get_board_size() + 1);
        threat = {curr}
        # check rows
        # left
        count = 1
        moves = 1
        while (curr - moves) % row_length == curr % row_length:
            if curr - moves in self.o:
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
        while (curr + moves) % row_length == curr % row_length:
            if curr + moves in self.o:
                threat.append(curr - moves)
                moves += 1
                count += 1
            elif curr + moves in self.f:
                threat.append(curr - moves)
                break
            else:
                break

        if count == 3 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack
        elif count == 4 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack

        return stack

    def check_columns(self, curr, stack):
        row_length = sqrt(self.get_board_size() + 1);
        threat = {curr}
        # check columns
        # down
        count = 1
        moves = 1
        while curr - moves * row_length >= 0:
            if curr - moves * row_length in self.o:
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
        while curr + moves * row_length < row_length ^ 2:
            if curr + moves * row_length in self.o:
                threat.append(curr - moves * row_length)
                moves += 1
                count += 1
            elif curr + moves * row_length in self.f:
                threat.append(curr - moves * row_length)
                break
            else:
                break

        if count == 3 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack
        elif count == 4 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack

        return stack

    def check_diag(self, curr, stack):
        row_length = sqrt(self.get_board_size() + 1);
        threat = {curr}
        r = curr % row_length
        c = curr - r * row_length
        # check left to right
        # down
        count = 1
        moves = 1
        while r - moves >= 0 and c + moves < row_length:
            if (r - moves) * row_length + (c + moves) in self.o:
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
            if (r + moves) * row_length + (c - moves) in self.o:
                threat.append((r + moves) * row_length + (c - moves))
                moves += 1
                count += 1
            elif (r + moves) * row_length + (c - moves) in self.f:
                threat.append((r + moves) * row_length + (c - moves))
                break
            else:
                break

        if count == 3 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack
        elif count == 4 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack

        threat = {curr}
        # check right to left
        # down
        count = 1
        moves = 1
        while r - moves >= 0 and c - moves >= 0:
            if (r - moves) * row_length + (c - moves) in self.o:
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
            if (r + moves) * row_length + (c + moves) in self.o:
                threat.append((r + moves) * row_length + (c + moves))
                moves += 1
                count += 1
            elif (r + moves) * row_length + (c + moves) in self.f:
                threat.append((r + moves) * row_length + (c + moves))
                break
            else:
                break

        if count == 3 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack
        elif count == 4 and len(threat) == 5:
            self.threats.append(threat)
            stack = threat ^ stack

        return stack

    def generate_threats(self):
        stack = self.o[:]
        while len(stack) != 0:
            curr = stack.pop()
            stack = self.check_rows(curr, stack)
            stack = self.check_columns(curr, stack)
            stack = self.check_diag(curr, stack)


class ABP(Agent):
    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        root = Node(None, None, None, None, -1)

        return choice(list(state.board.valid_actions))
