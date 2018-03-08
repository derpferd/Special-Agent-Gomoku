import mlp
from layer import Layer


_input = [1, 2, 3]
print(_input)

l = Layer(3, _input)
print(l.weights_matrix())

print(l.output())

m = mlp.Mlp(2, _input)
print(m)
