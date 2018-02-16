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

    def get_board_size(self):
        return max(max(self.p, self.o), self.f)

    def generate_threats(self):
        row_length = sqrt(self.get_board_size() + 1);
        # check rows
        s = 0

        # check columns
        s = 0

        # check left diagonals
        s = self.get_board_size() + 1 - row_length

        # check right diagonals
        s = self.get_board_size()
        for r in range()

class ABP(Agent):
    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        return choice(list(state.board.valid_actions))
