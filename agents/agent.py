# Author: Jonathan Beaulieu
from typing import List

from gym_gomoku import GomokuState


class Agent:
    def start_game(self, action_space: List[int]) -> None:
        """This function is run anytime a new game is started.

        Args:
            action_space: A list of all the possible actions that the game ever uses.
        """
        raise NotImplemented("Please implement in child class")

    def end_game(self, won: bool) -> None:
        """This function is run after game is done.

        Args:
            won: True if this agent won the game otherwise False.
        """
        raise NotImplemented("Please implement in child class")

    def move(self, state: GomokuState) -> int:
        """This function is called everything your bot needs to make a move.

        Args:
            state: The current state of the game at the start of this agents move.

        Returns:
            An int representing the action to make.
        """
        raise NotImplemented("Please implement in child class")

    def save_model(self, dirpath: str) -> None:
        """Optional function to save any model that was 'learned'.

        Args:
            dirpath: The path to the directory in which to save the data.
        """
        pass

    def load_model(self, dirpath: str) -> None:
        """Optional function to load a saved model.

        Args:
            dirpath: The path to the directory in which the data was saved.
        """
        pass
