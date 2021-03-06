
class Mlp:

    def __init__(self, layers):
        self.layers = layers

    def output(self, input_vector):
        output = self.layers[0].output_(input_vector)
        #print("Layers: ", 0, " ", self.layers[0])
        for i in range(1, len(self.layers)):
            output = self.layers[i].output_(output)
            #print("Layers: ", i, " ", self.layers[i])
        return output[0]

    def __repr__(self):
        s = "\n"
        for layer in self.layers:
            s += str(layer)
            s += "\n"
        return s

    @staticmethod
    def vector(state):
        vector = []
        for row in state.board.board_state:
            for col in row:
                vector.append(col)
        return vector
