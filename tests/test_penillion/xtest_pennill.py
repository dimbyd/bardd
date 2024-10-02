# test_pennill.py
# mae angen splitio!
import pytest

from bardd.llinell import Llinell
from bardd.pennill import Pennill

from bardd.pennill import prawf_englyn, prawf_hir_a_thoddaid
from bardd.allbwn import show_dadansoddiad_pennill

englyn_inputs = [
    ("Deunaw oed yn ei hyder, - deunaw oed\nYn ei holl ysblander,\nDy ddeunaw oed boed yn bêr,\nYn baradwys ddibryder."),
    ("Wele rith fel ymyl rhod - o'n cwmpas,\nCampwaith dewin hynod;\nHen linell bell nad yw'n bod,\nHen derfyn nad yw'n darfod."),
    ("Rhwydd gamwr, hawdd ei gymell - i'r mynydd\nA'r mannau anghysbell;\nHel a didol diadell\nYw camp hwn yn y cwm pell."),
    ("Yma mae angerdd i mi - i ennill\nsy'n anodd heb ferwi;\n A challio cyn ei cholli\nMewn crys coch yn groch ei gri"),
]

hat_inputs = [
    ("A thwym ddwyfron y gwneuthum ddiofryd\nI garu fy mhau fel gwyrf fy mywyd;\nAnwylo gwylltineb tir fy mebyd,\nEi lwyn a'i afon a'i lynnau hefyd.\nAc yn nyfnder ei weryd - gwn y caf\nEi gusan olaf megis anwylyd."),
    ("Tra bo dynoliaeth fe fydd amaethu\nA chyw hen linach yn ei olynu,\nA thra bo gaeaf bydd cynaeafu,\nA byw greadur tra bo gwerydu,\nBydd ffrwythlonder tra pery - haul a gwlith,\nYn wyn o wenith rhag ein newynnu."),
]

@pytest.mark.parametrize("test_input", englyn_inputs)
def test_englyn(test_input):
    llinellau = [Llinell(s) for s in test_input.split('\n')]
    pennill = Pennill(llinellau)
    dad = prawf_englyn(pennill)
    # print(show_dadansoddiad_pennill(dad))
    if 'notes' in dad:
        print('notes: {}'.format(dad['notes']))
    assert dad['dosbarth'] == 'ENG'

@pytest.mark.parametrize("test_input", hat_inputs)
def test_hat(test_input):
    llinellau = [Llinell(s) for s in test_input.split('\n')]
    pennill = Pennill(llinellau)
    dad = prawf_hir_a_thoddaid(pennill)
    if 'notes' in dad:
        print('notes: {}'.format(dad['notes']))
    assert dad['dosbarth'] == 'HAT'