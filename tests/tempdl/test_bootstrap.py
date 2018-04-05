from agents.tempdl.model.bootstrap import Bootstrap
from agents.tempdl.model.perceptron import Perceptron
from agents.tempdl.model.layer import Layer


def test_create():
    m = Bootstrap.create_mlp(1, 2, 2)
    m.output([1, 5])


def test_perceptron_output():
    p = Perceptron([2, 3], 4)
    output = p.output_([2, 3])
    assert output == 17


def test_layer_output():
    p1 = Perceptron([2, 3], 4)
    p2 = Perceptron([1, 2], 3)
    l = Layer([p1, p2])
    output = l.output_([2, 2])

    # 2*2 + 2*3 + 4 = 14
    # 2*1 + 2*2 + 3 = 11
    expected = [14, 9]
    result = output == expected
    # put assert here
