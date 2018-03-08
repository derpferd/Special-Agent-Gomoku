import mlp
from layer import Layer
from bootstrap import Bootstrap

m = Bootstrap.create_mlp(2, 3, 4)
print(m)