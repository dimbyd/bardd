# test_sain_odl_gudd.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Eu plaid yw duw rhai drwy'u hoes"),
    ("Llyfrdra dy wlad nid yw les"),
    ("A'i gord yn deffro'r dyffryn"),
    ("Aeth Idris draw'n drist gan drawster"),
    ("Nid â dy gariad o gof"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_sain_odl_gudd(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == 'SAI'