# test_cwpled.py
import pytest

from bardd.llinell import Llinell
from bardd.cwpled import oes_cwpled

test_inputs = [

    # cwpled cywydd
    ("Hen linell bell nad yw'n bod,\nHen derfyn nad yw'n darfod.", 'CWC'),

    # toddaid byr
    ("Talog, boed law, boed heulwen, - y saif hi\nEr oes faith, anniben;", 'TOB'),
    ("Deunaw oed yn ei hyder, - deunaw oed\nYn ei holl ysblander,", 'TOB'),
    ("Rhwydd gamwr, hawdd ei gymell - i'r mynydd\n A'r mannau anghysbell;", 'TOB'),
    ("Wele rith fel ymyl rhod - o'n cwmpas,\nCampwaith dewin hynod;", 'TOB'),
    ("Yma mae angerdd i mi - i ennill\nsy'n anodd heb ferwi", 'TOB'),

    # toddaid
    ("Wedi blwng ymosod blin, - encilio:\nWedi'n creithio dianc i'r eithin.", 'TOD'),
    ("A'u gweld yn eu dillad gwaith - trwy'r oriau\nYn rhwygo o greigiau eu goreugwaith.", 'TOD'),
    ("Mab Rhys aeth o'i lys i lawr - yr Erwig:\nMewn gro a cherrig mae'n garcharawr.", 'TOD'),

    # toddaid hir
    ("Ac yn nyfnder y weryd - gwn y caf\nEi gusan olaf megis anwylyd.", 'TOH'),
    ("Mae antur dan y mintys - ac anial\n Yw'r creithiau mâl lle bu'r crythau melys.", 'TOH'),
]

@pytest.mark.parametrize("test_input", test_inputs)
def test_cwpled(test_input):
    s = test_input[0].split('\n')
    x = Llinell(s[0])
    y = Llinell(s[1])
    dad = oes_cwpled(x,y)
    assert dad['dosbarth'] == test_input[1]