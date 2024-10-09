# dilyswr_llinellau.py
"""
Dulliau ar gyfer darganfod cynghanedd mewn llinell.

Sut mae peidio dychwelyd gwall e.e. "dim cyfatebiaeth dan yr acen"
pan yn profi safle gorffwysfa sydd yn anghywir? Os oes
dadansoddiad ddilys, mae'n bosib hidlo rhain "after the event" ,
ond sut mae dewis "Amwys" dros "Gwallus" pan nad yw'r
dilyswr yn darganfod unrhyw batrwm o gwbl?

Os yw'r orffwysfa yn y lle cywir, yna basai "crych a llyfn" yn
achosi'r gwall "dim cyfatebiaeth dan yr acen": oes angen cofnodi'r
ddau? Falle bod angen sticio gyda'r gwallau swyddogol, a profi
popeth arall cyn dychwelyd `dad.dosbarth = None`.

"""

from bardd.cysonion import geiriau_gwan
from bardd.llinell import Llinell
from bardd.odl import prawf_odl
from bardd.cytseinedd import prawf_cytseinedd, aceniad
from bardd.seineg import seinegoli

from bardd.dadansoddiad import Dadansoddiad
from bardd.cysonion import colormaps

from bardd.cysonion import max_cytseiniaid_pengoll

import logging
log = logging.getLogger(__name__)


# dadansoddi
def prawf_cynghanedd_gytsain(geiriau):
    """
    Gwirio am gynghanedd gytsain (croes, traws, neu ran o linell sain)
    Mewnbwn: Rhestr geiriau
    Allbwn:  Dadansoddiad (dict)

    Mae'r weithdrefn yma yn derbyn rhestr geiriau ac yn 
    profi pob safle posib am orffwysfa.
    """

    dad = Dadansoddiad()

    x_geiriau = []
    y_geiriau = list(geiriau)  # copi

    prifodl = y_geiriau[-1]  # gair olaf
    nifer_sillafau = 0

    # oes_gorffwysfa ar ol? (o'r chwith i'r dde)
    while y_geiriau:

        nesaf = y_geiriau.pop(0)  # pop o'r blaen
        x_geiriau.append(nesaf)

        # check nifer sillau hyd yma
        nifer_sillafau += nesaf.nifer_sillafau()
        if (prifodl.acennog() and nifer_sillafau > 4) \
                or (not prifodl.acennog() and nifer_sillafau > 3):

            log.info(f'Gorffwysfa wedi mynd yn rhy bell: {x_geiriau[-1]}')
            break

        # atal gorffwysfa ar eiriau gwan
        if str(nesaf) in geiriau_gwan:
            continue

        # profi am gytseinedd
        dad = prawf_cytseinedd(x_geiriau, y_geiriau)

        # llwyddiant
        if dad.dosbarth:
            dad.gorffwysfa = [nesaf],
            dad.aceniad = aceniad(nesaf, prifodl),
            if dad.dosbarth in ['CRO', 'COG']:
                return dad

    # traws?
    return dad


# def prawf_croes(geiriau):
#     dad = prawf_cynghanedd_gytsain(geiriau)
#     if dad.dosbarth in ["CRO", "COG", "CRG"]:
#         return dad
#     return None


# def prawf_traws(geiriau):
#     dad = prawf_cynghanedd_gytsain(geiriau)
#     if dad.dosbarth in ["TRA", "TRF", "TRG", "TRD"]:
#         return dad
#     return None


# def prawf_llusg(geiriau):
#     prifodl = geiriau[-1]

#     # rhaid i'r brifodl for yn air lluosill
#     if prifodl.nifer_sillafau() < 2:
#         log.info("Rhaid i'r brifodl fod yn air lluosill")
#         return None

#     # iteru dros eiriau'r linell i ddarganfod yr orffwysfa
#     # does dim angen "y_nesaf" os yw'r sillau yn barod wedi
#     # cael eu rhag-brosesu!?

#     for gorffwysfa in geiriau[:-1]:
#         log.debug(gorffwysfa.llinyn() + "/" + prifodl.llinyn())

#         # check am air gwan
#         if gorffwysfa.llinyn() in geiriau_gwan:
#             continue

#         # gwirio am odl lusg
#         dad = prawf_odl(gorffwysfa, prifodl, odl_lusg=True)

#         # dychewlyd dadansoddiad os oes odl lusg
#         if dad and dad.dosbarth in ["OLU", "OLL"]:
#             dad.gorffwysfa = [gorffwysfa],

#         return None

#     # dim
#     return None

def prawf_croesdraws(x1, x2):

    # Hidlo cyfatebiaeth anghytbyws acennog (AAAC)
    if not x1[-1].acennog() and x2[-1].acennog():
        return None

    dad = prawf_cytseinedd(x1, x2)
    print('dad_croesdraws: ', dad.dosbarth)
    
    # Hidlo cyfatebiaeth lararog (mae angen cyfateb o leiaf un gytsain)
    if dad.dosbarth:
        if dad.dosbarth in ['LLA']:
            return None

        return dad
    
    return None

# def prawf_traws(geiriau):
#     dad = prawf_cynghanedd_gytsain(geiriau)
#     if dad.dosbarth in ["TRA", "TRF", "TRG", "TRD"]:
#         return dad
#     return None


def prawf_llusg(x1, x2):

    dad_odl = prawf_odl((x1[-1], x2[0]), x2[-1], odl_lusg=True)

    if dad_odl.dosbarth in ["OLU", "OLL"]:

        dad = Dadansoddiad()
        dad.dosbarth = "LLU" if dad_odl.dosbarth == 'OLU' else 'LLL'
        dad.odl = dad_odl
        return dad

    return None


def prawf_sain(x1, x2, x3):

    # print(x1, x2, x3)

    # TODO: odl gudd rhwng x2 a x3
    dad_odl12 = prawf_odl((x1[-1], x2[0]), x2[-1], trwm_ac_ysgafn=False)
    # print('dad_odl12: ')
    # print('dosb: ', dad_odl12.dosbarth)
    # print(dad_odl12.nodau)

    if dad_odl12 and dad_odl12.dosbarth in ["OGY", "OLA"]:

        dad_cyts23 = prawf_cytseinedd(x2, x3)
        # print('dad_cyts23: ',  dad_cyts23)

        if dad_cyts23 and dad_cyts23.dosbarth:
            dad = Dadansoddiad()
            dad.odl = dad_odl12
            dad.cytseinedd = dad_cyts23

            if dad.cytseinedd.dosbarth == "LLA":
                dad.dosbarth = "SAL"  # sain lafarog

            elif "cyfateb" in dad.cytseinedd.nodau:
                if dad.cytseinedd.dosbarth == "COG":
                    dad.dosbarth = "SOG"  # sain o gyswllt
                else:
                    dad.dosbarth = "SAI"  # sain

            return dad
    return None


def prawf_llinell(llinell, min_sillafau=4, max_sillafau=10, trwm_ac_ysgafn=False, seinegol=True):
    """
    Profi am gynghanedd (omnibus)

    Mewnbwn:    Llinell
    Allbwn:     Dadansoddiad

    ** Dwy ran: x1, x2
    croes/traws:
        cytseinedd rhwng x1, x2
    llusg:
        odl lusg rhwng x1, x2

    ** Tair rhan: x1, x2, x3
    sain:
        odl rhwng x1, x2
        cytseinedd rhwng x2, x3
    llusg deirodl:
        odl rhwng x1, x2
        odl lusg rhwng x2 a x3 (a hefyd x1 a x3)

    ** Pedair rhan: x1, x2, x3, x4
    sain gadwynog:
        odl rhwng x1, x3
        cytseinedd rhwng x2, x4
    sain deirodl:
        odl rhwng x1, x2
        odl rhwng x2 a x3
        cytseinedd rhwng x3 a x4

    ** Pump rhan: x1, x2, x3, x4, x5
    sain ddwbl
        sain rhwng x1, x2, x3
        sain rhwng x3, x4, x5

    """

    # type check
    if not type(llinell) is Llinell:
        raise ValueError("Mae angen `Llinell` fan hyn.")

    # seinegoli
    dad_seinegol = None
    if seinegol:
        dad_seinegol = seinegoli(llinell)

    # init rhestr dadansoddiadau
    # mae rhai llinellau yn cynnwys dau neu dri math o gynghanedd
    dads = []

    # profi nifer sillafau
    if llinell.nifer_sillafau() < min_sillafau:
        gwall = 'Dim digon o sillafau: {} (min: {})'.format(llinell.nifer_sillafau(), min_sillafau)
        dad = Dadansoddiad(llinell)
        dad.dosbarth = 'GWA'
        dad.gwallau.append(gwall)
        return [dad]

    if llinell.nifer_sillafau() > max_sillafau:
        gwall = 'Gormod o sillafau: {} (max: {})'.format(llinell.nifer_sillafau(), max_sillafau)
        dad = Dadansoddiad(llinell)
        dad.dosbarth = 'GWA'
        dad.gwallau.append(gwall)
        return [dad]

    # alias
    geiriau = llinell.children
    nifer_geiriau = len(geiriau)

    # iteru dros safleoedd posib yr orffwysfa gyntaf
    for idx1 in range(1, nifer_geiriau):
        x1 = geiriau[:idx1]  # rhan gyntaf y linell
        x2 = geiriau[idx1:]  # ail ran

        # dilysu
        if not x1 or not x2:
            continue

        # print('(x1,x2) = ', (x1, x2))

        # hepgor geiriau gwan ar yr orffwysfa
        if str(x1[-1]).lower() in geiriau_gwan:
            continue

        # --------------------
        # 1. Profi am gynghanedd gytsain
        dad_cyts12 = prawf_cytseinedd(x1, x2)

        if dad_cyts12.dosbarth:  # llwyddiant

            # creu dadansoddiad newydd
            dad = Dadansoddiad(llinell)

            # dosbarth cytseinedd
            dad.dosbarth = dad_cyts12.dosbarth

            # atodi'r dadansoddiad cytseinedd
            dad.cytseinedd = dad_cyts12
            dad.gwallau += dad_cyts12.gwallau

            # cofnodi'r orffwysfa
            dad.gorffwysfeydd = (x1[-1],)

            # Profi am traws fantach (mae'n dibynnu ar safle'r orffwysfa)
            if dad.dosbarth == 'TRA':
                if (
                    (len(x1) == 1 and x1[0].nifer_sillafau() == 1) or
                    (len(x1) == 2 and x1[0].nifer_sillafau() == 1 and x1[1].nifer_sillafau() == 1 and
                        not any(nod.is_cytsain() for nod in geiriau[0].nodau()))
                ):
                    dad.dosbarth = 'TRF'

            # Hidlo cyfatebiaeth lararog (mae angen cysefeillio o leiaf unwaith)
            if dad.dosbarth in ['LLA']:
                pass

            # Hidlo cyfatebiaeth anghytbyws acennog (AAC)
            elif not x1[-1].acennog() and x2[-1].acennog():
                pass

            else:
                dads.append(dad)  # cofnodi'r dadansoddiad

        # --------------------
        # 2. Profi am gynghanedd lusg
        dad_odl = prawf_odl((x1[-1], x2[0]), x2[-1], odl_lusg=True, trwm_ac_ysgafn=True)
        if dad_odl and dad_odl.dosbarth in ["OLU", "OLL"]:
            dad = Dadansoddiad(llinell)
            dad.dosbarth = "LLU" if dad_odl.dosbarth in ['OLU', 'OLL'] else 'LLL'
            dad.odl = dad_odl           # dadansoddiad odl
            dad.gorffwysfeydd = (x1[-1],)
            # print('dad_llusg = ', dad_odl)
            dads.append(dad)

        # --------------------
        # 3. Dwy orffwysfa: cynghanedd sain neu lusg deirodl

        # iteru dros safleoedd posib yr ail orffwysfa (x1 heb newid)
        for idx2 in range(idx1 + 1, nifer_geiriau):
            x2 = geiriau[idx1:idx2]
            x3 = geiriau[idx2:]

            # dilysu
            if not x2 or not x3:
                continue

            # print('(x1,x2,x3) = ', (x1, x2, x3))

            # hepgor geiriau gwan ar yr orfwysfa
            if str(x2[-1]).lower() in geiriau_gwan:
                continue

            # profi am odl rhwng y ddwy ran gyntaf (TODO: odl gudd rhwng x2 a x3)
            dad_odl12 = prawf_odl((x1[-1], x2[0]), (x2[-1], x3[0]))
            # print("dad_odl12: ", dad_odl12)

            if dad_odl12 and dad_odl12.dosbarth in ["OGY", "OLA"]:

                # 3a sain: profi am gytseinedd rhwng yr ail a'r drydedd ran
                dad_cyts23 = prawf_cytseinedd(x2, x3)
                # print(x2, x3)
                # print("dad_cyts23: ", dad_cyts23.dosbarth)
                # print(dad_cyts23)

                if dad_cyts23 and dad_cyts23.dosbarth:
                    dad = Dadansoddiad(llinell)
                    dad.odl = dad_odl12
                    dad.cytseinedd = dad_cyts23

                    if dad.cytseinedd.dosbarth == "GWA":
                        dad.dosbarth = "GWA"  # gwallus

                    elif dad.cytseinedd.dosbarth == "LLA":
                        dad.dosbarth = "SAL"  # sain lafarog

                    elif "cyfateb" in dad_cyts23.nodau:
                        if dad.cytseinedd.dosbarth == "COG":
                            dad.dosbarth = "SOG"  # sain o gyswllt
                        else:
                            # print('FAN HYN')
                            dad.dosbarth = "SAI"  # sain

                    dad.gorffwysfeydd = (x1[-1], x2[-1])
                    # print('*** DAD ***: ', dad)
                    # print('*** dad.dosbarth ***: ', dad.dosbarth)
                    dads.append(dad)

                # 3b llusg deirodl:
                # profi am odl lusg rhwng yr ail a'r drydedd ran
                dad_odl23 = prawf_odl((x2[-1], x3[0]), x3[-1], odl_lusg=True)

                if dad_odl23.dosbarth in ["OLU", "OLL"]:
                    dad = Dadansoddiad(llinell)
                    dad.dosbarth = 'LLD'  # llusg deirodl
                    dad.odl = dad_odl12
                    dad.odl.hysbys += dad_odl23.hysbys
                    dad.odl.nodau += dad_odl23.nodau
                    dad.gorffwysfeydd = (x1[-1], x2[-1])
                    
                    dads.append(dad)
            
            # --------------------
            # 4. Pedair rhan: sain gadwynog a sain deirodl

            # iteru dros safleoedd posib y drydedd orffwysfa (x1 a x2 heb newid)
            for idx3 in range(idx2 + 1, nifer_geiriau):
                x3 = geiriau[idx2:idx3]
                x4 = geiriau[idx3:]

                # print('(x1,x2,x3,x4) = ', (x1,x2,x3,x4))

                # dilysu
                if not x3 or not x4:
                    continue

                # hepgor geiriau gwan ar yr orfwysfa
                if str(x3[-1]) in geiriau_gwan:
                    continue

                # --------------------
                # 4a Sain gadwynog
                #  un prawf odl: [x1, x3], un prawf cytseinedd: [x2, x4]

                # profi am odl rhwng rhan 1 a rhan 3
                dad_odl13 = prawf_odl((x1[-1], x2[0]), x3[-1])
                dad_cyts24 = prawf_cytseinedd(x2, x4)
                if dad_odl13 and dad_odl13.dosbarth in ["OGY", "OLA"] and dad_cyts24.dosbarth:

                    # mae angen o leiaf un par o gytseiniaid cyfatebol am SGA
                    if dad_cyts24 and 'cyfateb' in dad_cyts24.nodau and dad_cyts24.nodau['cyfateb']:

                        # llwyddiant
                        dad = Dadansoddiad(llinell)
                        dad.dosbarth = "SGA"
                        dad.odl = dad_odl13
                        dad.cytseinedd = dad_cyts24
                        dad.gorffwysfeydd = (x1[-1], x2[-1], x3[-1])
                        dads.append(dad)

                # --------------------
                # 4b sain deirodl (TODO: cudd am yr ail orffwysfa)
                # odl rhwng x1 a x2, odl rhwng x2 a x3, cytseinedd rhwng x3 a x4
                dad_odl12 = prawf_odl((x1[-1], x2[0]), x2[-1])
                dad_odl23 = prawf_odl((x2[-1], x3[0]), x3[-1])
                dad_cyts34 = prawf_cytseinedd(x3, x4)

                if (
                    dad_odl12 and dad_odl12.dosbarth in ["OGY", "OLA"] and
                    dad_odl23 and dad_odl23.dosbarth in ["OGY", "OLA"] and
                    dad_cyts34 and dad_cyts34.dosbarth
                ):
                    dad = Dadansoddiad(llinell)
                    dad.dosbarth = "SDO"
                    dad.odl = dad_odl12
                    dad.odl.hysbys += dad_odl23.hysbys
                    dad.odl.nodau += dad_odl23.nodau
                    dad.cytseinedd = dad_cyts34
                    dad.gorffwysfeydd = (x1[-1], x2[-1], x3[-1])
                    dads.append(dad)

                #--------------------
                # 5. Pump rhan: profi am sain ddwbl (TODO)
                # dau brawf sain: [x1,x2,x3] a [x3, x4,x5]

                # iteru dros safleoedd posib y bedwaredd orffwysfa
                for idx4 in range(idx3 + 1, nifer_geiriau):
                    x3 = geiriau[idx2:idx3]
                    x4 = geiriau[idx3:idx4]
                    x5 = geiriau[idx4:]

                    # print('(x1,x2,x3,x4,x5) = ', (x1,x2,x3,x4,x5))
                    # print('SDD', (x1, x2, x3, x4, x5))
                    dad123 = prawf_sain(x1, x2, x3)
                    dad345 = prawf_sain(x3, x4, x5)
                    sain = ['SAI', 'SOG', 'SAL']
                    if dad123 and dad123.dosbarth in sain and dad345 and dad345.dosbarth in sain:
                        dad = Dadansoddiad(llinell)
                        dad.dosbarth = "SDD"
                        dad.hysbys = dad123.hysbys + dad345.hysbys
 
                        dad.odl = dad123.odl
                        dad.odl.hysbys += dad345.odl.hysbys
                        dad.odl.nodau += dad345.odl.nodau
 
                        dad.cytseinedd = dad123.cytseinedd
                        dad.cytseinedd.hysbys += dad345.cytseinedd.hysbys
                        for key in dad.cytseinedd.nodau:
                            if key in dad345.cytseinedd.nodau:
                                dad.cytseinedd.nodau[key] += dad345.cytseinedd.nodau[key]
 
                        dad.gorffwysfeydd = (x1[-1], x2[-1], x3[-1], x4[-1])
                        dads.append(dad)
    # ----------
    # atodi hysbys y seinegoli
    if dad_seinegol:
        for dad in dads:
            dad.hysbys.extend(dad_seinegol.hysbys)

    # # dadansoddiad terfynol
    # print('==========')
    # for dad in dads:
    #     print(dad.adroddiad())
    #     print('=====')
    # print('==========')

    # hidlo

    # dileu traws bengoll
    # if len(dads) > 1 and any([dad.dosbarth in ['TBG'] for dad in dads]):
    #     dads = [dad for dad in dads if dad.dosbarth not in ['TBG']]

    # dileu croes/traws pengoll rhy hir
    if len(dads) > 1 and any([dad.dosbarth in ['CBG', 'TBG'] for dad in dads]):
        # dads = [dad for dad in dads if dad.dosbarth not in ['CBG']]
        dads = [
            dad
            for dad in dads
            if dad.dosbarth not in ['CBG', 'TBG'] or
            (dad.nodau and 'pengoll' in dad.nodau and
            len(dad.nodau['pengoll']) < max_cytseiniaid_pengoll)
        ]

    # hidlo dosbarthiadau gwallus os oes llwyddiant rhywle arall
    if any([dad.dosbarth not in ['GWA'] for dad in dads]):
        dads = [dad for dad in dads if dad.dosbarth not in ['GWA']]

    # hidlo sain pan mae sain ddwbl neu sain gadwynog
    if any([dad.dosbarth in ['SDD', 'SGA'] for dad in dads]):
        dads = [dad for dad in dads if dad.dosbarth not in ['SAI', 'SAL', 'TRF']]

    # hidlo sain a llusg pan mae llusg deirodl neu sain deirodl
    if any([dad.dosbarth in ['LLD', 'SDO'] for dad in dads]):
        dads = [dad for dad in dads if dad.dosbarth not in ['SAI', 'SAL', 'LLU', 'LLL']]
    
    # hidlo traws pan mae croes
    if any([dad.dosbarth in ['CRO', 'COG', 'CRD', 'CRG'] for dad in dads]):
        dads = [dad for dad in dads if dad.dosbarth[:2] not in ['TR', 'TF']]

    # print('>>>>>>>>>1', dads)
    # os heb ddarganfod dim ....
    if not dads:
        return [Dadansoddiad(llinell)]  # null

    # print('>>>>>>>>>2', dads)
    return dads

    # dim dadansoddiad
    if not dads:
        return [Dadansoddiad(llinell)]

    # un dadansoddiad
    elif len(dads) == 1:
        return dads

    # dau ddadansoddiad
    else:
        # return dads[0]
        # hack er mwyn cael croes cyn traws
        dads.sort(key=lambda x1: x1.dosbarth)

        # mae sain gadwynog hefyd yn sain
        if dads[0].dosbarth != 'SGA' and dads[1].dosbarth == 'SGA':
            dads.reverse()

        croes = ['CRO', 'CRD', 'CRG', 'COG', 'CGD', 'CGG']
        traws = ['TRA', 'TRD', 'TRG', 'TRF', 'TFD', 'TFG']
        llusg = ['LLU', 'LLA']
        sain = ['SAI', 'SOG', 'SAD', 'SAG', 'SGA', 'SAL']

        dosb1 = dads[0].dosbarth
        dosb2 = dads[1].dosbarth

        # print('dosb = ', (dosb1, dosb2))

        # defnyddio'r dadansoddiad cyntaf fel sylfaen
        dad = dads[0]

        # bail out!
        # return dad


        # croes
        if dosb1 in croes:
            if dosb2 in traws:
                dad.dosbarth = 'TGR'  # trawsgroes
            elif dosb2 in sain:
                dad.dosbarth = 'SGR'  # seingroes
            elif dosb2 in llusg:
                dad.dosbarth = 'CLU'  # croeslusg
            else:
                pass  # croes

        # sain
        elif dosb1 in sain:
            if dosb1 == 'SGA':
                dad.dosbarth = 'SGA'  # bail out
            # elif dosb1 == 'SOG':
            #     dad.dosbarth = 'SOG'  # bail out
                # if dosb2 in croes:
                #     dad.dosbarth = 'SGG'  # saing gadwynog groes
                # elif dosb2 in traws:
                #     dad.dosbarth = 'SGD'  # sain gadwynog draws
                # elif dosb2 in llusg:
                #     dad.dosbarth = 'SGL'  # sain gadwynog lusg
                # else:
                #     dad.dosbarth = 'SOG'  # sain gadwynog
            else:
                if dosb2 in croes:
                    dad.dosbarth = 'SGR'  # seingroes
                elif dosb2 in traws:
                    dad.dosbarth = 'SDR'  # seindraws
                elif dosb2 in llusg:
                    dad.dosbarth = 'SLU'  # seinlusg
                else:
                    pass  # sain

        # llusg
        elif dosb1 in llusg:
            if dosb2 in croes:
                dad.dosbarth = 'CLU'  # croeslusg
            elif dosb2 in traws:
                dad.dosbarth = 'TLU'  # trawslusg
            elif dosb2 in sain:
                dad.dosbarth = 'SLU'  # seinlusg
            else:
                pass  # llusg

        # traws
        elif dosb1 in traws:
            if dosb2 in croes:
                dad.dosbarth = 'TGR'  # trawsgroes
            elif dosb2 in sain:
                dad.dosbarth = 'SDR'  # seindraws
            elif dosb2 in llusg:
                dad.dosbarth = 'TLU'  # trawslusg
            else:
                pass  # traws

        # cofnodi yr ail odl
        if hasattr(dads[1], 'odl'):
            dad.odl2 = dads[1].odl

        # cofnodi yr ail gytseinedd
        if hasattr(dads[1], 'cytseinedd'):
            dad.cytseinedd2 = dads[1].cytseinedd

    # # atodi hysbys y seinegoli
    # if dad_seinegol:
    #     dad.hysbys.extend(dad_seinegol.hysbys)

    # diwedd (dadansoddiad gyfunol)
    return [dad]

    # A ddylen ni ddychwelyd pob dadansoddiad dilys?

# ------------------------------------------------
def main():

    from bardd.data_llinellau import profion

    profion['problem'] = (
        "Canlyniad cariad yw cosb",
        "Awdur mad a dramodydd",               # rhy gynnar
        "Ymysg y bedw yn ddedwydd",            # w-gytsain
    )

    for key in [
            # 'croes',
            # 'traws',
            # 'llusg',
            # 'sain',
            # 'croes_o_gyswllt',
            # 'sain_o_gyswllt',
            # 'sain_gadwynog',
            # 'trychben',
            # 'cysylltben',
            # 'traws_fantach',
            # 'llusg_lafarog',
            # 'llusg_gudd',
            # 'llusg_ewinog',
            # 'sain_gudd', 
            # 'sain_ewinog',
            # 'sain_lafarog',
            # 'seingroes',
            # 'trawsgroes',
            # 'seindraws',
            # 'croeslusg',
            # 'seinlusg',
            # 'trawslusg',
            # 'misc',
            # 'sain_siwr',
            # 'problem',
            # 'aberteifi',
            # 'randoms',
            # 'llusg_deirodl',
            # 'sain_deirodl',
            # 'sain_ddwbl',
            # 'check_me',
            # 'check_metoo',
            # 'ac_nid_ag',
            # 'sicr_wallus',
            'posib_wallus',
    ]:

        print(key.upper())
        # print('\n\n==============================')
        # print('***', key.upper(), '***')
        # print('==============================')
        for s in profion[key]:

            ll = Llinell(s)

            print('--------------------------------------------')
            # print(ll)
            seinegoli(ll, meddalu=True, caledu=-True)
            # print(repr(ll))
            # print('---')
            # print(ll.sain())
            # print(ll.nifer_geiriau())
            # print(ll.nifer_sillafau())
            # print(ll.children[0].children[0])

            dads = prawf_llinell(ll, trwm_ac_ysgafn=False)

            # print('uned:', dad.uned)
            # print('sain:', dad.uned.sain())

            if not dads:
                dad = Dadansoddiad(ll)
                # print(dad.fancy())
                print(dad.beiro.magenta('dim'))

            for dad in dads:
                # print(dad.beiro.cyan(llythrenwau["cynghanedd"][dad.dosbarth]))
                print(dad.fancy(cmap=colormaps['disglair']))
                # print(dad.dosbarth)
                # if dad and hasattr(dad, 'odl') and dad.odl:
                #     print('odl.dosbarth:', dad.odl.dosbarth)
                #     print('odl.nodau:', dad.odl.nodau)
                #     if dad.odl.hysbys:
                #         print('odl.hysbys:', dad.odl.hysbys)

                # if dad and hasattr(dad, 'cytseinedd'):  # and dad.cytseinedd and dad.cytseinedd.dosbarth != 'LLA':
                #     print('cyts.dosbarth:', dad.cytseinedd.dosbarth)
                #     print('cyts.nodau:', dad.cytseinedd.nodau)
                #     if dad.cytseinedd.hysbys:
                #         print('cyts.hysbys:', dad.cytseinedd.hysbys)

                if not dad == dads[-1]:
                    print('---')
        return None
    
        print('--------------------------------------------')
        from bardd.gair import Gair
        from bardd.sillaf import Sillaf
        s1 = 'Boch'
        s2 = 'goch'
        s3 = 'gain'
        s1 = 'gain'
        s2 = 'rhiain'
        s3 = 'rywiog'
        x1 = [Gair(s1)]
        # x2 = [Gair(s2)]
        # x3 = [Gair(s3)]
        
        sillA = Sillaf(cyrch='rh', cnewyllyn='iai', coda='n')
        g2 = Gair()
        g2.children.append(sillA)
        x2 = [g2]
        
        sillC = Sillaf(cyrch='r', cnewyllyn='yw', coda='')
        sillD = Sillaf(cyrch='', cnewyllyn='io', coda='g')
        g3 = Gair()
        g3.children.append(sillC)
        g3.children.append(sillD)
        x3 = [g3]
        
        print('Fan hyn: ', x1 + x2 + x3)
        dad = prawf_sain(x1, x2, x3)
        print(dad.dosbarth)
        print(dad.adroddiad())


if __name__ == '__main__':

    # llinell unigol
    # from bardd.gair import Gair
    
    # s1 = "A chlytwaith"
    # s2 = "taith"
    # s3 = "i'n tywys"

    # s1 = "A daw'n glir"
    # s2 = "fod byd dan glo,"

    # # a = [Gair(s) for s in s1.split()]
    # # b = [Gair(s) for s in s2.split()]
    # # c = [Gair(s) for s in s3.split()]

    # # # dad = prawf_sain(a, b, c)
    # # dad = prawf_croesdraws(a, b)
    # # print('dad pcd:', dad.dosbarth)
    # # if dad:
    # #     print(dad.adroddiad())

    # ll = Llinell(' '.join([s1, s2]))
    # ll = Llinell("O dad yn deulu dedwydd")
    # ll = Llinell("A daw'n glir fod byd dan glo,")
    # ll = Llinell("Yn awr i'r pair. A'i apêl")

    # print('====================')
    # print(ll)
    # dads = prawf_llinell(ll)
    # print('dads = ', dads)
    # print('dad pll:', [dad.dosbarth for dad in dads])
    # for dad in dads:
    #     print(dad.fancy())
    #     print(dad.adroddiad())
    #     # print(dad.cytseinedd)


    main()
