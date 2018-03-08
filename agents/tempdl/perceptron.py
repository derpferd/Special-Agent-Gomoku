from random import random


class Perceptron:
    def __init__(self, _input, weights=None, bias=None):
        self._input = _input
        self.weights = weights
        self.bias = bias
        if self.weights is None or bias is None:
            self.__random_weights()

    def __random_weights(self):
        self.weights = [random() for _ in range(len(self._input))]
        self.bias = random()

    def __repr__(self):
        s = "\n================== Perceptron ======================\n"
        s += "\n======= weights ======\n"
        s += str(self.weights)
        s += "\n==== bias ====\n"
        s += str(self.bias)
        return s
