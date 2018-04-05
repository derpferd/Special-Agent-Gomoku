import numpy as np
from numpy.random.mtrand import RandomState

from . import perceptron
from . import layer
from . import mlp


class Bootstrap:
    def __init__(self):
        pass

    @staticmethod
    def create_perceptron_with_random_weights(n_weights, random: RandomState):
        weights = list(random.rand(n_weights))
        bias = random.rand()
        return perceptron.Perceptron(weights, bias)

    @staticmethod
    def create_layer(n_perceptrons, n_weights, random):
        return layer.Layer(Bootstrap.create_perceptron_with_random_weights(n_weights, random) for _ in range(n_perceptrons))

    @staticmethod
    def create_mlp(n_layers, n_perceptrons, n_weights, random=None):
        if random is None:
            random = np.random.RandomState()
        #changed this so it will work but unsure if it is correct
        #now the weights look like 361, 3 for each hidden layer, and 1 for output
        layers = [Bootstrap.create_layer(n_perceptrons, n_weights, random)] + \
                 [Bootstrap.create_layer(n_perceptrons, n_perceptrons, random) for _ in range(n_layers-1)] + \
                 [Bootstrap.create_layer(1, n_perceptrons, random)]  # output layer
        return mlp.Mlp(layers)

