# test_sain.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Cân ddiddig ar frig y fron"),
    ("Gŵr amhur yn sur ei sen"),
    ("Bydd y dolydd yn deilio"),
    ("Canlyniad cariad yw cosb"),
    ("Cân hardd croyw fardd Caerfyrddin"),
    ("Mae'n gas gennyf dras y dref"),
    ("Heddychwr gwr rhagorol"),
    ("Fe ddaeth pob croes i'w oes ef"),  # methiant
    ("Didranc ieuanc ei awen"),  # methiant
    ("Pren gwyrddliw o wiw wead"),  # methiant
    ("Gŵr o ystryw ydyw ef"),  # methiant
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_sain(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad["dosbarth"] == "SAI"
