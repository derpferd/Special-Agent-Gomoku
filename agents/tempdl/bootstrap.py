from perceptron import Perceptron
from random import random
from layer import Layer
from mlp import Mlp


class Bootstrap:
    def __init__(self):
        pass

    @staticmethod
    def create_perceptron_with_random_weights(n_weights):
        weights = [random() for _ in range(n_weights)]
        bias = random()
        return Perceptron(weights, bias)

    # n_weights is number of weights per perceptron
    @staticmethod
    def create_layer(n_perceptrons, n_weights):
        perceptrons = []
        for i in range(n_perceptrons):
            perceptrons.append(Bootstrap.create_perceptron_with_random_weights(n_weights))
        return Layer(perceptrons)

    @staticmethod
    def create_mlp(n_layers, n_perceptrons, n_weights):
        layers = []
        for i in range(n_layers):
            layers.append(Bootstrap.create_layer(n_perceptrons, n_weights))
        return Mlp(layers)
