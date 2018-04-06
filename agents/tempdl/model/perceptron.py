import numpy as np
from random import random


class Perceptron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
        self.prevoutput = 0
        self.curoutput = 0
        self.gradients = [[]]

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
        self.prevoutput = self.curoutput
        self.add_gradient()
        self.curoutput = np.maximum(output, 0)
        self.updateweights()
        return self.curoutput

    def updateweights(self):
        new_weights = []
        alpha = 0.7

        for i in len(self.weights):
            new_weights[i] = self.weights[i] + (alpha * (self.curoutput - self.prevoutput) * self.gradient_sum()[i])

    def add_gradient(self):
        new_gradient = self.calc_gradient()
        self.gradients.append(new_gradient)

    def calc_gradient(self):
        return [random() for i in len(self.weights)]

    def gradient_sum(self):
        arr = np.zeros(len(self.weights))
        for i in len(self.gradients):
            arr = np.add(arr, np.asarray(self.gradients[i]))
        return arr


