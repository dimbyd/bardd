# test_aceniad.py
import pytest
from bardd.gair import Gair
from bardd.acen import aceniad

test_inputs = [
	('ci','drwg', 'CAC'),
	('ci','drewllyd', 'ADI'),
	('blodyn','pert', 'ADY'),
	('blodyn','banana', 'CDI'),
]

@pytest.mark.parametrize("test_input", test_inputs)
def test_nifer_sillau(test_input):
    g0 = Gair(test_input[0])
    g1 = Gair(test_input[1])
    assert aceniad(g0, g1) == test_input[2]
