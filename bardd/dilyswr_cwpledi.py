# profwr_cwpledi.py
'''
Cwpled cywydd           CC7, CC4
Toddaid|byr|hir         TOD,TOB,TOH             # odl ac odl gyrch

Cwpled wythsill         CWS                     # y ddwy linell yn odli
Cwpled nawsill          CNS                     # y ddwy linell yn odli
Cwpled ddegsill         CDS                     # y ddwy linell yn odli
Cwpled cyhydedd hir:    CCH = [LL5,LL5,LL5,LL4]  # y tri rhan gyntaf yn odli
'''

from bardd.llinell import Llinell
from bardd.dadansoddiad import Dadansoddiad

from bardd.odl import prawf_odl
from bardd.dilyswr_llinellau import prawf_llinell


def prawf_cwpled(x, y):
    '''
    Profi am gwpled.
    '''
    dad = prawf_cwpled_cywydd(x, y)
    if dad.dosbarth == 'CC7':
        return dad
    return prawf_toddaid(x, y)


def prawf_cwpled_cywydd(x, y):
    '''
    Profi am gwpled cywydd.
    Mewnbwn: dau wrthrych `Llinell'
    Allbwn: `Dadansoddiad'
    '''

    # init
    dad = Dadansoddiad()

    # profi am saith sill yn y ddwy linell
    if x.nifer_sillafau() != 7:
        dad.hysbys.append('CC7: mae angen saith sill yn y linell gyntaf')
        return dad
    if y.nifer_sillafau() != 7:
        dad.hysbys.append('CC7: mae angen saith sill yn yr ail linell')
        return dad

    # profi am odl
    dad_odl = prawf_odl(x.prifodl(), y.prifodl())
    if dad_odl.dosbarth not in ['OGY', 'OLA']:
        dad.hysbys.append('CC7: dim odl')
        return dad

    # profi am gynghanedd yn y ddwy linell
    x_dad = prawf_llinell(x)
    if not x_dad.dosbarth:
        dad.hysbys.append('CC7: dim cynghanedd yn y linell gyntaf')
        return dad

    y_dad = prawf_llinell(y)
    if not y_dad.dosbarth:
        dad.hysbys.append('CC7: dim cynghanedd yn yr ail linell')
        return dad

    # cymharu acenionn brifodl yn acennog a'r llall yn ddiacen
    if x.prifodl().acennog() == y.prifodl().acennog():
        dad.gwallau.append('CC7: mae angen aceniad gwahanol yn y ddwy linell')
        return dad

    # profi nad oes cynghanedd lusg yn yr ail linell
    if y_dad.dosbarth in ['LLU', 'LLL']:
        dad.gwallau.append('CC7: dim hawl cael cynghanedd lusg yn yr ail linell')
        return dad

    # llwyddiant
    dad.dosbarth = 'CC7'
    dad.cyntaf = x_dad
    dad.ail = y_dad
    dad.odl = dad_odl
    return dad


def prawf_toddaid(x, y):
    '''
    Profi am doddaid byr, toddaid a thoddaid hir
    Mewnbwn: dau wrthrych `Llinell'
    Allbwn: `Dadansoddiad'
    '''
    # init
    dad = Dadansoddiad()

    # rhannu'r linell gyntaf
    blaen = []
    cyrch = []
    cysylltnod = False
    for gair in x.children:
        if gair.llinyn() == '-':
            cysylltnod = True
        elif not cysylltnod:
            blaen.append(gair)
        else:
            cyrch.append(gair)

    # print('blaen: {}'.format(blaen))
    # print('cyrch: {}'.format(cyrch))

    # profi am ddeg sill yn y linell gyntaf
    if x.nifer_sillafau() != 10:
        dad.hysbys.append('TOD: mae angen 10 sill yn y linell gyntaf')
        return dad

    # profi am gynghanedd yn y linell gyntaf
    x_dad = prawf_llinell(Llinell(blaen))
    if not x_dad.dosbarth:
        dad.hysbys.append('TOD: dim cynghanedd yn y linell gyntaf')
        return dad

    # profi am odl rhwng prifodl y gynghanedd gyntaf a diwedd yr ail linell
    dad_odl = prawf_odl(blaen[-1], y.prifodl())
    if not dad_odl.dosbarth:
        dad.hysbys.append('TOD: dim odl')
        return dad

    # profi am doddaid byr
    if y.nifer_sillafau() == 6:

        # profi am gynghanedd rhwng y cyrch a rhan gyntaf yr ail linell
        # does dim hawl cael cynghanedd lusg fan hyn!
        pont = list(cyrch)
        for gair in y.children:
            pont.append(gair)
            # print('pont: {}'.format(pont))
            y_dad = prawf_llinell(Llinell(pont))

            if y_dad.dosbarth:

                # methiant
                if y_dad.dosbarth not in ['LLU', 'LLL']:
                    dad.hysbys["TOB: cynghanedd Lusg rhwng cyrch y linell gyntaf a dechrau'r ail"]
                    return dad

                # llwyddiant
                dad.dosbarth = 'TOB'
                dad.cyntaf = x_dad
                dad.ail = y_dad
                dad.odl = dad_odl
                return dad

        # methiant
        dad.hysbys.append('TOB: dim cynghanedd yn yr ail ran.')
        return dad

    # profi am doddaid neu doddaid hir
    elif y.nifer_sillafau() in [9, 10]:

        # profi am gynghanedd yn yr ail linell
        y_dad = prawf_llinell(y)
        if not y_dad.dosbarth:
            dad.hysbys.append('TOD/TOH: dim cynghanedd yn yr ail linell')
            return dad

        # profi am odl rhwng cyrch y linell gyntaf a gorffwysfa'r ail linell
        # os oes mwy nag un gorffwysfa (sain), gall y cyrch odli
        # gyda unrhyw un o'r gorffwysfeydd
        if cyrch and 'gorffwysfa' in y_dad:

            for gorffwysfa in y_dad['gorffwysfa']:

                dad_odl_gyrch = prawf_odl(cyrch[-1], gorffwysfa)

                # tweak
                if not dad_odl_gyrch['dosbarth'] in ['SAI', 'SLA']:
                    continue

                # llwyddiant
                if y.nifer_sillafau() == 9:
                    dad.dosbarth = 'TOD'    # toddaid
                else:
                    dad.dosbarth = 'TOH'    # toddaid hir
                dad.cyntaf = x_dad
                dad.ail = y_dad
                dad.odl = dad_odl
                dad.odl_gyrch = dad_odl_gyrch
                return dad

            # methiant
            dad.hysbys.append('TOD/TOH: dim odl gyrch.')
            return dad

    # methiant
    else:
        dad.hysbys.append('TOD: rhaid cael 6, 9 neu 10 sill yn yr ail linell')
        return dad


# ------------------------------------------------
# main
def main():

    from bardd.beiro import Beiro
    brwsh = Beiro()

    test_data = {
        'cwpled_cywydd': (
            "Hen linell bell nad yw'n bod,\nHen derfyn nad yw'n darfod.",
        ),
        'toddaid': (
            "Wedi blwng ymosod blin, - encilio:\nWedi'n creithio dianc i'r eithin.",
            "A'u gweld yn eu dillad gwaith - trwy'r oriau\nYn rhwygo o greigiau eu goreugwaith.",
            "Mab Rhys aeth o'i lys i lawr - yr Erwig:\nMewn gro a cherrig mae'n garcharawr.",
        ),
        'toddaid_byr': (
            "Yma mae angerdd i mi - i ennill\nsy'n anodd heb ferwi",
            "Talog, boed law, boed heulwen, - y saif hi\nEr oes faith, anniben;",
            "Deunaw oed yn ei hyder, - deunaw oed\nYn ei holl ysblander,",
            "Rhwydd gamwr, hawdd ei gymell - i'r mynydd\n A'r mannau anghysbell;",
            "Wele rith fel ymyl rhod - o'n cwmpas,\nCampwaith dewin hynod;",
            "Yma mae angerdd i mi - i ennill\nsy'n anodd heb ferwi",
        ),
        'toddaid_hir': (
            "Ac yn nyfnder y weryd - gwn y caf\nEi gusan olaf megis anwylyd.",
            "Mae antur dan y mintys - ac anial\n Yw'r creithiau mâl lle bu'r crythau melys.",
        ),
    }

    for key in [
        'cwpled_cywydd',
        'toddaid_byr',
        'toddaid',
        'toddaid_hir',
    ]:
        print('========================================')
        print(key.upper())
        print('========================================')
        for cwp in test_data[key]:
            # call(["clear"])
            print('---------------')
            cwp = cwp.split('\n')
            x = Llinell(cwp[0])
            y = Llinell(cwp[1])
            print(x.llinyn_acenion())
            print(x)
            print(y.llinyn_acenion())
            print(y)

            dad = prawf_cwpled(x, y)
            if dad.dosbarth:
                print(brwsh.gwyrdd(dad.dosbarth))
            print(dad)
            # print('dad1: {}'.format(dad))
            # if not dad['dosbarth']:
            #     dad = oes_toddaid(x, y)
            # print('dad2: {}'.format(dad))
            # if dad['dosbarth']:
            #     # print(dad['dosbarth'])
            #     show(dad)
            #     print(cyan(dad['dosbarth']))
            # print('--------------------')
            # for key2 in ['dosbarth', 'dad_cyntaf', 'dad_ail', 'gorffwysfa']:
            #     if key2 in dad and dad[key2]:
            #         print('{} : {}'.format(key2, str(dad[key2])))
            # try:
            #     input(">> bwrwch y dychwelwr i barhau ...")
            # except KeyboardInterrupt:
            #     return
            # continue


if __name__ == '__main__':

    # s = "Hen linell bell nad yw'n bod,\nHen derfyn nad yw'n darfod."
    # cwp = [Llinell(ss) for ss in s.split('\n')]
    # dad = oes_cwpled(cwp[0], cwp[1])
    # print('dad: {}'.format(dad))

    main()
