# Author: Jonathan Beaulieu
from random import random
from typing import List

from gym_gomoku import GomokuState

from .. import Agent
from mlp import Mlp


class Tempdl(Agent):

    def start_game(self, action_space: List[int]) -> None:
        print('Tempdl agent starting:')
        self.mlp = None

    def end_game(self, won: bool) -> None:
        print('Game ended')
        if won == True:
            print('I won!')
        else:
            print('I lost!!')

    def move(self, state: GomokuState) -> int:
        maxvalue = -1
        selected_action = -1
        for action in state.board.valid_actions:
            value = self.evaluate(action, state)
            if value > maxvalue:
                maxvalue = value
                selected_action = action
        return selected_action

    def evaluate(self, action, state):
        # set state to state after action
        pass
