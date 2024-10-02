# test_sain_odl_ewinog.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Caf fynd draw ar hynt i'r rhos"),
    ("Rhoi het ar ei harffed hi"),
    ("Caf fynd tua'r helynt draw"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_sain_odl_ewinog(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell, seinegol=True)
    assert dad["dosbarth"] == "SAI"
