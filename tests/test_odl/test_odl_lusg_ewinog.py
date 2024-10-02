# test_odl_lusg_ewinog.py
import pytest

from bardd.gair import Gair
from bardd.odl import prawf_odl

test_inputs = [
    ('wyneb', 'haul', 'Epynt'),
    ('esgob', 'biau', 'popeth'),    # methiant
    ('nghariad', 'hyd', 'ato'),
    ('garreg', 'hon', 'eco'),
]

@pytest.mark.parametrize("test_input", test_inputs)
def test_odl_lusg_ewinog(test_input):
    g0 = Gair(test_input[0])
    g1 = Gair(test_input[1])
    g2 = Gair(test_input[2])
    dad = prawf_odl((g0, g1), g2, odl_lusg=True)
    assert dad['dosbarth'] == 'OLU'