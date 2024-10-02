# test_llusg_odl_gudd.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Ac yma bu cydnabod"),
    ("Ac wedi d'awr godidog"),
    ("Ac wele lid y gelyn"),
    ("Gwn ddifa lawer calon"),
    ("Eto dring lethr Carn Ingli"),
    ("Y ddinas draw yn wastraff"),
    ("Esgor mae llid ar ormes"),
    ("Bu llawer ddoe yn cerdded"),
    ("Dacw wiw dyfiant liwdeg"),
    ("Ac wele wychder Dewi"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_llusg_odl_gudd(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell, seinegol=True)
    assert dad['dosbarth'] == 'LLU'