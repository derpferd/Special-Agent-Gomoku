# Author: Jonathan Beaulieu
from typing import List

from .. import Agent
from gym_gomoku import GomokuState


class Random(Agent):
    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        return self.np_random.choice(list(state.board.valid_actions))
