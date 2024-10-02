# test_traws.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Ochain cloch a gwreichion clir"),
    ("Si'r oerwynt dan sêr araul"),
    ("Awdur mad yw'r dramodydd"),
    ("Ei awen brudd dros ein bro"),
    ("Ni all lladd ond ennyn llid"),      

    ("Y gŵr aruchel ei gân"),
    ("Y brawd o bellafion bro"),
    ("Brwd yw aderyn brig"),
    ("Glaw ar ymylon y glyn"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_traws(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == 'TRA'