# Author: Jonathan Beaulieu
from random import choice
from typing import List

from .. import Agent
from gym_gomoku import GomokuState


class Random(Agent):
    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        return choice(list(state.board.valid_actions))
