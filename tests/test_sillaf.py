# test_gair.py
import pytest
from bardd.gair import Gair

test_inputs = [
    ("cath", 1),
    ("helo", 2),
    ("duon", 2),  # deusain ddeusill
    ("anifeiliaid", 4),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_sillaf(test_input):
    gair = Gair(test_input[0])
    assert gair.nifer_sillafau() == test_input[1]
