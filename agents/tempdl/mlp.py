# Represent each board state as a feature vector of length 361
# Each where each index is a cell and the value of the index is
# based on what is in the cell, black, white, empty
# Initialize random weight vector and multiply to get the value of the state

from random import random
import perceptron


class Mlp:

    class Layer:
        def __init__(self, n_perceptrons, _input):
            self.layer = [perceptron.Perceptron(_input) for _ in range(n_perceptrons)]

        def __repr__(self):
            s = "\n =========================== Layer ======================================"
            for perceptron in self.layer:
                s += str(perceptron)
            return s

    def __init__(self, n_layers, _input):
        self.n_layers = n_layers
        self._input = _input
        self.layers = [self.Layer(len(_input), _input) for _ in range(n_layers)]

    def __repr__(self):
        s = "\n"
        for layer in self.layers:
            s += str(layer)
            s += "\n"
        return s

    def evaluate(self, state):
        vector = self.vector(state)
        return random()

    @staticmethod
    def vector(state):
        vector = []
        for row in state.board.board_state:
            for col in row:
                vector.append(col)
        return vector
