# Represent each board state as a feature vector of length 361
# Each where each index is a cell and the value of the index is
# based on what is in the cell, black, white, empty
# Initialize random weight vector and multiply to get the value of the state

from random import random
from layer import Layer


class Mlp:

    def __init__(self, n_layers, _input):
        self.n_layers = n_layers
        self._input = _input
        self.layers = []
        self.__create_layers()

    def __create_layers(self):
        layer = Layer(len(self._input), self._input)
        for i in range(self.n_layers):
            self.layers.append(layer)
            layer = Layer(len(layer.output()), layer.output())
        output_layer = Layer(1, self.layers[-1].output())
        self.layers.append(output_layer)

    def output(self):
        return self.layers[-1].output()

    def __repr__(self):
        s = "\n"
        for layer in self.layers:
            s += str(layer)
            s += "\n"
        return s

    @staticmethod
    def vector(state):
        vector = []
        for row in state.board.board_state:
            for col in row:
                vector.append(col)
        return vector
