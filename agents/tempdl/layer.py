from perceptron import Perceptron
import numpy as np


class Layer:
    def __init__(self, n_perceptrons, _input):
        self.n_perceptrons = n_perceptrons
        self._input = _input
        self.perceptrons = [Perceptron(_input) for _ in range(n_perceptrons)]

    def weights_matrix(self):
        weights_matrix = []
        for perceptron in self.perceptrons:
            weights_matrix.append(perceptron.weights)
        return np.array(weights_matrix)

    def output(self):
        weights_matrix = self.weights_matrix()
        bias_vector = [p.bias for p in self.perceptrons]
        r = np.matmul(weights_matrix, self._input)
        r = np.add(r, bias_vector)
        return r

    def __repr__(self):
        s = "\n =========================== Layer ======================================"
        for perceptron in self.perceptrons:
            s += str(perceptron)
        return s