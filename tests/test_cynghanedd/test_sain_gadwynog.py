# test_sain_gadwynog.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Dringo bryn a rhodio bro"),
    ("Trydar mwyn adar y mynydd"),
    ("Un dydd gwelais brydydd gwiw"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_sain_gadwynog(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == 'SAG'