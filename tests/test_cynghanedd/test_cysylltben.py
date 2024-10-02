# test_cysylltben.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Onid bro dy baradwys", 'CRO'),
    ("A ddaw fy mab i Ddyfed", 'TRA'),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_cysylltben(test_input):
    llinell = Llinell(test_input[0])
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == test_input[1]