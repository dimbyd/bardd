# test_croes.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Ochain cloch a chanu clir"),
    ("Si'r oerwynt a sêr araul"),
    ("Awdur mad a dramodydd"),
    ("Ei awen brudd yn eu bro"),
    ("Onid teg yw ein tud?"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_croes(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == 'CRO'