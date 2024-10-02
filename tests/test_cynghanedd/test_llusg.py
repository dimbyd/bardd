# test_llusg.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Beiddgar yw geiriau cariad"),
    ("Y mae arogl yn goglais"),
    ("Pell ydyw coed yr ellyll"),
    ("Y mae Morfudd yn cuddio"),
    ("Yr haul ar dawel heli"),
    ("Taw â'th sôn, gad fi'n llonydd"),
    ("Ymysg y bedw yn ddedwydd"),            # methiant
    ("Un distaw ei wrandawiad"),             # methiant              
    ("Gwynt y rhew yn distewi"),              
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_llusg(test_input):
    llinell = Llinell(test_input)
    dad = prawf_llinell(llinell)
    assert dad['dosbarth'] == 'LLU'
