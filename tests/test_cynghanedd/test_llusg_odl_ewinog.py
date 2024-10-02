# test_llusg_odl_gudd.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Yn wyneb haul ar Epynt"),
    ("Yr esgob biau popeth"),
    ("Aeth fy nghariad hyd ato"),
    ("O'r garreg hon daeth eco"),
    ("I'r esgob pur rhoed popeth"),
    ("Fy nghariad troaf atat"),
    ("O'r garreg clywaid eco"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_llusg_odl_ewinog(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad["dosbarth"] == "LLU"
