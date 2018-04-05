
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

    def updateweights(self):
