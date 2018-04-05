import numpy as np


class Perceptron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
        self.output = []

    def __repr__(self):
        s = "\n================== Perceptron ======================"
        s += "\n======= weights ======\n"
        s += str(self.weights)
        s += "\n==== bias ====\n"
        s += str(self.bias)
        return s

    def output_(self, input_vector):
        if len(input_vector) != len(self.weights):
            raise ValueError("dimensions for input and weights don't match")
        output = np.dot(input_vector, self.weights) + self.bias
        return np.maximum(output, 0)

    def updateweights(self):
        pass
