# Author: Jonathan Beaulieu
import string
from typing import List

from multiprocessing import Lock

from .. import Agent
from gym_gomoku import GomokuState


class Human(Agent):
    STARTED = Lock()

    def __init__(self, config):
        super().__init__(config)
        if not self.STARTED.acquire(False):
            raise Exception("The Human agent only supports a single human player.")

    def __del__(self):
        self.STARTED.release()
        super().__init__(self)

    def start_game(self, action_space: List[int]) -> None:
        pass

    def end_game(self, won: bool) -> None:
        pass

    def move(self, state: GomokuState) -> int:
        move = None
        while move is None:
            raw_move = input("Enter the position of your move: ").upper()
            try:
                raw_move = int(raw_move)
                if 0 <= raw_move <= 360:
                    row = raw_move // 19
                    col = raw_move % 19
            except ValueError:
                col = "".join(filter(lambda x: x in string.ascii_letters, raw_move))
                row = "".join(filter(lambda x: x in string.digits, raw_move))
                if len(col) + len(row) != len(raw_move):
                    print("Invalid move!")
                    continue
                try:
                    row = int(row) - 1
                except ValueError:
                    print("Invalid move!")
                    continue
                if len(col) != 1 or row < 0:
                    print("Invalid move!")
                    continue
                try:
                    col = string.ascii_uppercase.index(col)
                except ValueError:
                    print("Invalid move!")
                    continue
                if row >= state.board.size or col >= state.board.size:
                    print("Invalid move!")
                    continue

            coord = (row, col)
            action = state.coord_to_action(coord)
            if action not in state.empty:
                print("Move already taken!")
                continue
            move = action
        return move
