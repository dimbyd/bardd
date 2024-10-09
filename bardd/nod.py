"""
nod.py
    Nod: llythren (yn cynnwys deugraffau), gofod neu atalnod
"""
from bardd.base import TreeNode
from bardd.cysonion import \
    llafariaid, llafariaid_byr, \
    cytseiniaid, atalnodau, hir2byr

import logging
log = logging.getLogger(__name__)


class Nod(TreeNode):
    """
    Dosbarth i ddarlunio llythyren, gofod neu atalnod unigol.
    """

    def __init__(self, s=None, parent=None):
        TreeNode.__init__(self, parent=parent)
        self.text = s
        self.sain = self.text
        # log.debug("`Nod` created: {}".format(self))

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()

    def sain(self):
        return self.sain

    def xml(self):
        element = super().xml()
        element.text = self.text
        return element

    # Mae hwn er mwyn i (nod1 == nod2) weithio'n iawn
    # h.y. profi os ydy'r ddau newidyn yn cyfeirio at yr un gwrthrych.
    # Mae hyn yn galluogi defnyddio `nodau.index(nod)` er mwn darganfod
    # lleoliad y gwrthrych `nod` mewn rhestr o nodau, neu i ddileu
    # gwrthrychau penodol o restri nodau.
    # Er mwyn profi os yw gwerthoedd y nodau yn hafal, rhaid
    # defnyddio `nod1.text == nod2.text`

    def __eq__(self, other):
        return isinstance(other, Nod) and self is other

    def is_space(self):
        return self.text.isspace()

    def is_atalnod(self):
        return self.text in atalnodau

    def is_llafariad(self):
        return self.text in llafariaid

    def is_cytsain(self):
        # if self.text.lower() == 'h':
        #     return False
        return self.text in cytseiniaid

    def byr(self):
        if self.text in hir2byr:
            return Nod(hir2byr[self.text])
        return Nod(self.text)

    def is_byr(self):
        if self.sain in llafariaid_byr:
            return True
        return False


# ------------------------------------------------
# test
def main():

    from lxml import etree
    nod = Nod("ch")
    print(etree.tostring(nod.xml(), pretty_print=True))

    n1 = Nod("é")
    n2 = Nod("b")
    print(n1)
    print(n2)
    print(n1.byr())
    if n1.is_llafariad():
        print("Llafariad")
        print("Ysgafn") if n1.is_byr() else print("Trwm")


if __name__ == "__main__":
    main()
