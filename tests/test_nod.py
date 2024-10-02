# test_node.py

from bardd.nod import Nod


def test_space():
    nod = Nod(" ")
    assert nod.is_space() is True


def test_atalnod():
    nod = Nod(";")
    assert nod.is_atalnod() is True
