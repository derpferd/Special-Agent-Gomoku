# Author: Jonathan Beaulieu
from random import random
from typing import List

from gym_gomoku import GomokuState
# from bootstrap import Bootstrap
from utils import Verbosity
from .. import Agent
# from mlp import Mlp
from .model import bootstrap


class Tempdl(Agent):

    def start_game(self, action_space: List[int]) -> None:
        if self.config.verbose.at_level(Verbosity.info):
            print('Tempdl agent starting:')
        self.mlp = bootstrap.Bootstrap.create_mlp(2, 3, 361, self.np_random)

    def end_game(self, won: bool) -> None:
        if self.config.verbose.at_level(Verbosity.info):
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
        return random()
        pass
