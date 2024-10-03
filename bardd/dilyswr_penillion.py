# dilyswr_penillion.py
'''
Dulliau ar gyfer darganfod mesur barddonol mewn pennill

Cywydd deuair hirion:   CDH = [CC7,CC7,...]         
Cywydd deuair fyrion:   CDF = [CC4,CC4,...]         
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
from bardd.llinell import Llinell
from bardd.pennill import Pennill

from bardd.dadansoddiad import Dadansoddiad
from bardd.odl import prawf_odl
from bardd.dilyswr_llinellau import prawf_llinell
from bardd.dilyswr_cwpledi import prawf_cwpled_cywydd, prawf_toddaid


def prawf_pennill(pennill):
    '''
    Profi am fesur cynganeddol.
    Mae hwn yn cydlynnu y ffwythiannau penodol isod.
    '''

    dad = prawf_cywydd(pennill)
    if dad.dosbarth == 'CC7':
        return dad

    dad = prawf_englyn(pennill)
    if dad.dosbarth == 'EUU':
        return dad

    dad = prawf_hir_a_thoddaid(pennill)
    if dad.dosbarth == 'HAT':
        return dad

    dad = prawf_cyhydedd_nawban(pennill)
    if dad.dosbarth == 'CNB':
        return dad

    return None


def prawf_cywydd(pennill):

    # init
    dad = Dadansoddiad(pennill)

    llinellau = list(pennill.children)
    llinellau.reverse()  # ar gyfer popio

    # check
    if not llinellau or len(llinellau) % 2:
        dad.hysbys.append('CC7: llinell unigol')
        return dad

    # iteru dros cwpledi
    dad_fesul_cwpled = []
    while llinellau:
        cyntaf = llinellau.pop()
        ail = llinellau.pop()
        dad_cwpled = prawf_cwpled_cywydd(cyntaf, ail)
        if dad_cwpled.dosbarth != 'CC7':
            dad.hysbys.append('CC7: dim cwpled cywydd')
            return dad
        dad_fesul_cwpled.append(dad_cwpled)

    # llwyddiant
    dad.dosbarth = 'CC7'
    dad.cwpledi = dad_fesul_cwpled
    return dad


def prawf_englyn(pennill):

    # init
    dad = Dadansoddiad(pennill)

    llinellau = list(pennill.children)

    # check
    if not llinellau or len(llinellau) != 4:
        dad.hysbys.append('EUU: mae angen 4 llinell')
        return dad

    # paladr
    dad_paladr = prawf_toddaid(llinellau[0], llinellau[1])
    if dad_paladr.dosbarth == 'TOB':
        if dad_paladr.cyntaf.dosbarth in ['LLU', 'LLL']:
            dad.hysbys.append(
                'EUU: cynghanedd lusg rhwng y cyrch a\'r ail linell')
            return dad
    else:
        dad.hysbys.append('EUU: dim toddaid byr yn y baladr')
        return dad

    # esgyll
    dad_esgyll = prawf_cwpled_cywydd(llinellau[2], llinellau[3])
    if dad_esgyll.dosbarth == 'CC7':
        if dad_esgyll.ail.dosbarth in ['LLU', 'LLL']:
            dad.hysbys.append('EUU: cynghanedd lusg yn y llinell olaf')
            return dad
    else:
        dad.hysbys.append('EUU: dim cwpled cywydd yn yr esgyll')
        return dad

    # profi odlau
    if not prawf_odl(llinellau[0], llinellau[1]).dosbarth in ['OGY', 'OLA']:
        dad.hysbys.append('EUU: dim odl yn y baladr')
        return dad

    elif not prawf_odl(llinellau[2], llinellau[3]).dosbarth in ['OGY', 'OLA']:
        dad.hysbys.append('EUU: dim odl yn yr esgyll')
        return dad

    elif not prawf_odl(llinellau[1], llinellau[3]).dosbarth in ['OGY', 'OLA']:
        dad.hysbys.append("EUU: dim odl rhwng y paladr a'r esgyll")
        return dad

    # llwyddiant
    dad.dosbarth = 'EUU'
    dad.cwpledi = [dad_paladr, dad_esgyll]
    return dad


def prawf_hir_a_thoddaid(pennill):

    # init
    dad = Dadansoddiad(pennill)

    llinellau = list(pennill.children)

    # check
    if not llinellau or len(llinellau) % 2 != 0:
        dad.hysbys.append('HAT: llinell unigol.')
        return dad

    # creu rhestr cwpledi
    llinellau.reverse()
    cwpledi = []
    while llinellau:
        cyntaf = llinellau.pop()
        ail = llinellau.pop()
        cwpledi.append([cyntaf, ail])

    # profi'r cwpledi ar wahan i'r olaf
    dad_fesul_cwpled = []
    for cwpled in cwpledi[:-1]:

        # nifer sillau
        if cwpled[0].nifer_sillafau() != 10 or cwpled[1].nifer_sillafau() != 10:
            dad.hysbys.append(
                "HAT: mae angen 10 sill ym mhob llinell ar wahan i'r olaf")
            return dad

        # profi cynghanedd
        dad_cwpled = prawf_cwpled_cywydd(cwpled[0], cwpled[1])
        if not dad_cwpled.dosbarth == 'CC7':
            dad.hysbys.append('HAT: dim cwpled cywydd')
            return dad

        # check odl
        dad_odl = prawf_odl(cwpled[0].prifodl(), cwpled[1].prifodl())
        if not dad_odl.dosbarth:
            dad.hysbys.append('HAT: dim odl')
            return dad

        dad_fesul_cwpled.append(dad_cwpled)

        # profi am doddaid hir yn cwpled olaf
        dad_toddaid = prawf_toddaid(cwpledi[-1][0], cwpledi[-1][1])
        if not dad_toddaid.dosbarth or not dad_toddaid.dosbarth == 'TOD':
            dad.hysbys.append('HAT: dim toddaid yn y gwpled olaf')
            return dad

        dad_fesul_cwpled.append(dad)

    # llwyddiant
    dad.dosbarth = 'HAT'
    dad.cwpledi = dad_fesul_cwpled
    return dad


def prawf_cyhydedd_nawban(pennill):

    # init
    dad = Dadansoddiad(pennill)

    llinellau = list(pennill.children)
    dad_fesul_llinell = []

    # nifer llinellau
    if not llinellau or len(llinellau) != 4:
        dad.hysbys.append('CNB: dim 4 llinell')
        return dad

    # profi llinellau unigol
    for llinell in llinellau:

        # nifer sillau
        if llinell.nifer_sillafau() != 9:
            dad.hysbys.append('CNB: dim naw sill ym mhob llinell')
            return dad

        # cynghanedd
        dad_llinell = prawf_llinell(llinell)
        if not dad_llinell.dosbarth:
            dad.hysbys.append('CNB: dim cynghanedd (%s)' % llinell.llinyn())
            return dad

    # profi odl
    for j in range(len(llinellau) - 1):
        dad_odl = prawf_odl(llinellau[j].prifodl(), llinellau[j + 1].prifodl())
        if not dad_odl.dosbarth:
            dad.hysbys.append('CNB: dim odl')

    # llwyddiant
    dad.dosbarth = 'CNB'
    dad.llinellau = dad_fesul_llinell

    return dad


# ------------------------------------------------
# main
def main():

    from bardd.data_penillion import profion
    from bardd.beiro import Beiro
    brwsh = Beiro()

    for key in [
        'cywydd',
        # 'englyn',
        # 'cyhydedd_nawban',
        # 'hir_a_thoddaid',
    ]:

        print('========================================')
        print(key.upper())
        print('========================================')
        for p in profion[key]:
            # call(["clear"])
            llinellau = [Llinell(s) for s in p.split('\n')]
            for ll in llinellau:
                print(ll.llinyn_acenion())
                print(str(ll))

            pennill = Pennill(llinellau)
            dad = prawf_pennill(pennill)
            if dad and dad.dosbarth:
                print(brwsh.gwyrdd(dad.dosbarth))
            else:
                print(brwsh.coch('DIM'))

            # show(dad, verbose=False)
            if dad:
                print(dad)
            
            print('---------------')


if __name__ == '__main__':

    main()

    # s = "Pa eisiau dim hapusach,\nNa byd yr aderyn bach?\nByd o hedfan a chanu\nA hwylio toc i gael tu."

    # print(s.split('\n'))
    # llinellau = [Llinell(ss) for ss in s.split('\n')]
    # pennill = Pennill(llinellau)
    # dad = prawf_mesur(pennill)
    # print(dad)

    # from lxml import etree
    # xtree = pennill.xml()
    # print(xtree)
    # s = etree.tostring(xtree, pretty_print=True)
    # print(s)
