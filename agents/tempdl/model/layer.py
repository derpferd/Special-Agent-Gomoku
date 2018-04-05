
import numpy as np


class Layer:

    def __init__(self, perceptrons):
        self.perceptrons = list(perceptrons)

    def __weights_matrix(self):
        weights_matrix = []
        for _perceptron in self.perceptrons:
            weights_matrix.append(_perceptron.weights)
        return np.array(weights_matrix)

    def output(self, input_vector):
        weights_matrix = self.__weights_matrix()
        bias_vector = [p.bias for p in self.perceptrons]

        if len(input_vector) != len(weights_matrix[0]):
            raise ValueError("dimensions for input and weights don't match")
        r = np.matmul(weights_matrix, input_vector)
        if len(r) != len(bias_vector):
            raise ValueError("dimensions of matrix multiplication result and bias don't match")
        r = np.add(r, bias_vector)
        r = np.maximum(r, 0)
        return r

    def __repr__(self):
        s = "\n =========================== Layer ======================================"
        for _perceptron in self.perceptrons:
            s += str(_perceptron)
        return s