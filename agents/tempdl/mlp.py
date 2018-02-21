###Represent each board state as a feature vector of length 361
###Each where each index is a cell and the value of the index is
###based on what is in the cell, black, white, empty
###Intialize random weight vector and multiply to get the value of the state
class Mlp:
    def __init__(self):
        self.layers = []

    def predict(self):
        print("Predict called")
