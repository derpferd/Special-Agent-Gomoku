import mlp
from layer import Layer


_input = [0, 1, 2, 1, 0, 2]
print(_input)

m = mlp.Mlp(2, _input)
print(m)
