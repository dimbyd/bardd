# test_odl_lusg_gudd.py
import pytest

from bardd.gair import Gair
from bardd.odl import prawf_odl

test_inputs = [
    ("yma", "bu", "cydnabod"),
    ("wele", "lid", "gelyn"),
    ("ddifa", "lawer", "calon"),
    ("wiw", "dyfiant", "liwdeg"),
    ("ddinas", "draw", "wastraff"),
    ("wele", "wychder", "Dewi"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_odl_lusg_gudd(test_input):
    g0 = Gair(test_input[0])
    g1 = Gair(test_input[1])
    g2 = Gair(test_input[2])
    dad = prawf_odl((g0, g1), g2, odl_lusg=True, trawsff=True)
    assert dad["dosbarth"] == "OLU"
