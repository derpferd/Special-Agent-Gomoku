
from bootstrap import Bootstrap

m = Bootstrap.create_mlp(1, 2, 2)
print(m)
print(m.output([1, 5]))
