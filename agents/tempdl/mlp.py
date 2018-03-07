###Represent each board state as a feature vector of length 361
###Each where each index is a cell and the value of the index is
###based on what is in the cell, black, white, empty
###Intialize random weight vector and multiply to get the value of the state

from random import random


class Mlp:
    def __init__(self):
        self.layers = []
        #load layer weights from file

    def evaluate(self, state):
        vector = self.vector(state)
        return random()

    def vector(self, state):
        vector = []
        for row in state.board.board_state:
            for col in row:
                vector.append(col)

        #print("=============================\n")
        #print(vector)
        #print("==============================\n")

        return vector
