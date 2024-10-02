# test_sain_o_gyswllt.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Galarnad groch a chloch leddf"),
    ("Bydd sug i'r grug a'r egin"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_sain_o_gyswllt(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == 'SOG'