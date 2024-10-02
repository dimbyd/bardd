# test_llinell.py
import pytest
from bardd.llinell import Llinell

test_inputs = [
    ("O dad, yn deulu dedwydd", 7),
    ("Lle i enaid gael llonydd", 7),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_nifer_sillafau(test_input):
    ll = Llinell(test_input[0])
    assert ll.nifer_sillafau() == test_input[1]
