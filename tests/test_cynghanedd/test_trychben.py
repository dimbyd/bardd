# test_trychben.py
import pytest

from bardd.llinell import Llinell
from bardd.profwr_llinellau import prawf_llinell

test_inputs = [
    ("Canu mydr cyn ymadael", "CRO"),
    ("Nid yn aml y down yma", "CRO"),
    ("Ond daw gwefr cyn atgofion", "TRA"),  # methiant (dim caledu d+d->t ?)
    ("Calon ddofn ei hofn hefyd", "SAI"),
    ("Parabl anabl anniben", "SAI"),  # methiant: cam-acennu "anabl"
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_trychben(test_input):
    llinell = Llinell(test_input[0])
    dad = prawf_llinell(llinell)
    assert dad["dosbarth"] == test_input[1]
