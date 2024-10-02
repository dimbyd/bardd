# test_odl_lusg.py
import pytest

from bardd.gair import Gair
from bardd.odl import prawf_odl

test_inputs = [
    ("beiddgar", "cariad"),
    ("morfudd", "cuddio"),
    ("tawel", "heli"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_odl(test_input):
    g0 = Gair(test_input[0])
    g1 = Gair(test_input[1])
    dad = prawf_odl(g0, g1, odl_lusg=True)
    assert dad["dosbarth"] == "OLU"
