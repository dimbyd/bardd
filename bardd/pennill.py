# pennill.py
'''
Cywydd deuair hirion:   CDH = [CC7,CC7,...]
Cywydd deuair fyrion:   CDH = [CC4,CC4,...]
Englyn unodl union:     EUU = [TOB,CWC]             # pob llinell yn odli
Englyn crwca:           ECR = [CWC,TOB]             # pob llinell yn odli
Englyn milwr:           EMI = [LL7,LL7,LL7]         # pob llinell yn seithsill ac yn odli
Englyn penfyr:          EPF = [TOB,LL7]             # pob llinell yn odli
Cyhydedd nawban:        CYN = [CNS,CNS]             # pob llinell yn nawsill ac yn odli
Cyhydedd fer:           CYF = [CWS,CWS]             # pob llinell yn wythsill ac yn odli
Cyhydedd hir:           CYH = [CCH,CCH[,CCH,...]]   # pob llinell yn odli
Gwawdodyn byr:          GWB = [CNS,TOD]             # pob llinell yn odli
Gwawdodyn hir:          GWH = [CNS,CNS,TOD]         # pob llinell yn odli, dim cynghanedd lusg yn y llinell olaf
Hir a thoddaid:         HAT = [CDS,CDS[,CDS],TOH]   # pob llinell yn odli
'''

from bardd.base import TreeNode

# from bardd.dadansoddiad import Dadansoddiad

# from bardd.odl import oes_odl
# from bardd.cynghanedd import oes_cynghanedd
# from bardd.cwpled import oes_cwpled_cywydd, oes_toddaid

# from bardd.allbwn import show_dadansoddiad_cwpled, show_dadansoddiad_pennill


class Pennill(TreeNode):
    '''
    Pennill fel rhestr o wrthrychau
    `Llinell` neu `Cwpled` mewn unrhyw drefn.
    '''

    def __init__(self, unedau, parent=None):
        TreeNode.__init__(self, parent=parent)
        self.children = unedau

    def __str__(self):
        return '\n'.join([str(uned) for uned in self.children])

    def __repr__(self):
        return '\n'.join([repr(uned) for uned in self.children])

    def nifer_unedau(self):
        return len(self.children)
