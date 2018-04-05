from agents.tempdl.model.bootstrap import Bootstrap


def test_create():
    m = Bootstrap.create_mlp(1, 2, 2)
    m.output([1, 5])
