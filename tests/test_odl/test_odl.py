# test_odl.py
import pytest

from bardd.gair import Gair
from bardd.odl import prawf_odl

test_inputs = [
    # dim
    ("beic", "haul", None),
    ("buwch", "rhyfedd", None),
    # odlau_cyflawn
    ("cath", "math", "OGY"),
    ("pren", "llen", "OGY"),
    ("mafon", "duon", "OGY"),  # deusain ddwbl
    ("calon", "creulon", "OGY"),
    ("gwlad", "cariad", "OGY"),
    ("galwad", "cariad", "OGY"),  # dwy ddeusiain talgron
    ("wiwd", "liwd", "OGY"),
    ("croes", "oes", "OGY"),
    # odlau_llafarog
    ("tro", "llo", "OLA"),
    ("cadno", "banjo", "OLA"),
    # proestau_cyflawn
    ("hen", "dyn", "PGY"),
    ("llawn", "mewn", "PGY"),
    ("telyn", "ystyrlon", "PGY"),
    # proestau_llafarog
    ("tew", "byw", "PLA"),
    ("bro", "da", "PLA"),
]


@pytest.mark.parametrize("test_input", test_inputs)
def test_odl(test_input):
    g0 = Gair(test_input[0])
    g1 = Gair(test_input[1])
    dad = prawf_odl(g0, g1)
    assert dad["dosbarth"] == test_input[2]
