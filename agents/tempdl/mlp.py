# Represent each board state as a feature vector of length 361
# Each where each index is a cell and the value of the index is
# based on what is in the cell, black, white, empty
# Initialize random weight vector and multiply to get the value of the state

from random import random


class Mlp:
    class Perceptron:
        def __init__(self, weights, bias):
            self.weights = weights
            self.bias = bias

        def __repr__(self):
            s = "\n======= weights ======\n"
            s += str(self.weights)
            s += "\n==== bias ====\n"
            s += str(self.bias)
            return s

    def __init__(self, n_layers, input_size):
        self.layers = []
        self.n_layers = n_layers
        self.input_size = input_size
        self.__random_weights()

    def __random_weights(self):
        weights = [random() for _ in range(self.input_size)]
        for x in range(self.n_layers):
            p = self.Perceptron(weights, random())
            self.layers.append(p)

    def __repr__(self):
        s = "\n"
        for x in self.layers:
            s += str(x)
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
