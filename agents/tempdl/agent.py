# Author: Jonathan Beaulieu
from random import choice
from typing import List
from random import random

from .. import Agent
from gym_gomoku import GomokuState


class Tempdl(Agent):
    def start_game(self, action_space: List[int]) -> None:
        print('Tempdl agent starting:')

    def end_game(self, won: bool) -> None:
        print('Game ended')
        if won:
            print('I won!')
        else:
            print('I lost!')

    def move(self, state: GomokuState) -> int:
        # random = choice(list(state.board.valid_actions))
        # return random

        maxvalue = -1
        selected_action = -1
        for action in state.board.valid_actions:
            value = self.evaluate(action, state)
            if value > maxvalue:
                maxvalue = value
                selected_action = action
        return selected_action

    def evaluate(self, action, state):
        return random()
