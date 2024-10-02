# test_croes_o_gyswllt.py
import pytest

from bardd.llinell import Llinell
from bardd.cynghanedd import prawf_cynghanedd

test_inputs = [
    ("Aderyn llwyd ar un llaw"),
    ("Daw geiriau Duw o'i gaer deg"),     
    ("Rhwydd gamwr, hawdd ei gymell"),
    ("Gwr enwog yw o ran gwaith"),        # methiant
]

@pytest.mark.parametrize("test_input", test_inputs)
def test_croes_o_gyswllt(test_input):
    llinell = Llinell(test_input)
    dad = prawf_cynghanedd(llinell)
    assert dad['dosbarth'] == 'COG'