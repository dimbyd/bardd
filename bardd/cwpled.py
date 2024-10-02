# cwpled.py
'''
Cwpled cywydd           CC7, CC4
Toddaid|byr|hir         TOD,TOB,TOH             # odl ac odl gyrch
Cwpled wythsill         CWS                     # y ddwy linell yn odli
Cwpled nawsill          CNS                     # y ddwy linell yn odli
Cwpled degsill          CDS                     # y ddwy linell yn odli
Cwpled Cyhydedd hir:    CCH = [LL5,LL5,LL5,LL4]  # y tri rhan gyntaf yn odli
'''

from bardd.base import TreeNode
from bardd.llinell import Llinell


class Cwpled(TreeNode):
    '''
    Cwpled ar ffurf rhestr o ddau `Llinell`.
    '''

    def __init__(self, cyntaf, ail, parent=None):
        TreeNode.__init__(self, parent=parent)

        if not (type(cyntaf) is Llinell and type(ail) is Llinell):
            raise ValueError('Mae angen dau `Llinell` i wneud `Cwpled')

        self.children = [cyntaf, ail]

    def cyntaf(self):
        return self.children[0]

    def ail(self):
        return self.children[1]

    def __str__(self):
        return ''.join([str(llinell) for llinell in self.children])

    def __repr__(self):
        return ''.join([repr(llinell) for llinell in self.children])
