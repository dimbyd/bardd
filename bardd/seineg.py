# seinegoli.py
"""
Dulliau trawsnewid text i sain (sillafu ffonetig)

Mewnbwn: `uned` sef `Gair`, `Llinell`, `Cwpled` neu `Pennill`
Allbwn: `None`

    - meddalu t -> d, c -> g, p -> b
    - odlau ewinog (caledu oherwydd cytsain gyntaf y gair olynol)
    - cywasgu cytseiniaid ddwbl
    e.e. ninnau, barri (un-yn-ateb-dau mewn odl)

meddalu:
    c + a -> g  e.e. ac aderyn
    p + i -> b  e.e. ap ifan

    wastraff -> wasdraff
    speshal -> sbeshal

Wyddor Gymraeg -> Wyddor Phonetic -> Audio?

    Trawsnewid unedau testunol i unedau ffonetig
    cywasgu: cael gwared ar gytseiniaid dwbl
    meddalu: s+t -> s+d, s+c -> s+g, s+p -> s+b ayb
    caledu: b+h -> p+h, b+b -> p+p, g+h -> c+h, d+h->t+h ayb

    Mae angen seinegoli llinellau, cwpledi a phenillion, 
    Oes angen seinegoli ar draws lllinellau? (oes)
    
    ----- 
    Mae gan pob `Nod` y briodwedd `nod.sain` sydd yn cofnodi 
    sain y nod, ochr yn ochr gyda'r text valuwe.
    
    Dylai pob penderfyniad o ran odl a chytseinedd gael eu gwneud ar
    sail yr uned seiegol.

    Mae hyn hefyd yn wir am y nodau dethol: mae cytseinio ac
    odli yn digwydd ar draws llinellau, ac mae angen cadw nodau
    dethol y llinell ar wahan i nodau dethol y cwpled
    neu bennill.

    Felly pan mae `Nod` yn cael ei greu tra'n creu llinell,
    cwpled neu bennill, mae'r nod wedi ei glymmu i'r uned,
    gan y bydd `nod.sain` yn dibynnu ar y nodau blaenorol
    a dilynnol o fewn yr uned.

    nod.text()
    nod.sain()

    Ar y lefel isaf tra'n profi am odl neu gytseinedd, rydym ni
    bob amser yn y pendraw yn cymharu llinynnau, nid gwrthrychau.

    g = Gair('shwmae')
    str(g)      # llinyn
    repr(g)     # fesul sill, ffonetig hefyd?


"""

from bardd.cysonion import cytseiniaid_meddalu, cyfatebiaeth_meddal, cyfuniadau_caled, cyfuniadau_trychben

from bardd.nod import Nod
from bardd.sillaf import Sillaf
from bardd.gair import Gair
from bardd.llinell import Llinell
from bardd.pennill import Pennill

from bardd.uned import Uned

from bardd.dadansoddiad import Dadansoddiad

def odlau_deheuol(uned, hct=False):
    """ Ydy e mor hawdd ag ailosod pob 'u' ac 'y' gyda 'i'?
    """
    pass

def seinegoli_fesul_sillaf(uned, cywasgu=True, meddalu=True, caledu=True):
    """
    Trawsnewid unedau i fersiynau ffonetig
    cywasgu: cael gwared ar gytseiniaid dwbl
    meddalu: s+t -> s+d, s+c -> s+g, s+p -> s+b ayb
    caledu: b+h -> p+h, b+b -> p+p, g+h -> c+h, d+h->t+h ayb

    Mae angen seinegoli llinellau, cwpledi a phenillion, a dim
    gwahanu mewn i eiriau ac yna 'seinegoli ar draws y bwlch'.
    fel mae pethe ar hyn o bryd.
    Mae siwr o fod hefyd angen seinegoli ar draws lllinellau.

    Mae gan bob gwrthrych `Nod` ddau briodwedd:
        Nod.text
        Nod.sain
    Mae'r seinegoli yn dibynnu ar nodau sy'n dod cyn
    neu ar ol y nod o fewn y frawddeg.

    Pan mae gwrthrych `Nod` yn cael ei greu tra'n creu 
    gwrthrych `Gair`, `Llinell`, `Cwpled` neu `Pennill`,
    rhaid i'r nod yna bob amser berthyn i'r uned honno, 
    gan y bydd `nod.text_seinegol` yn
    dibynnu ar y nodau cyn ac/neu ar ol y nod yn yr uned.

    Bydd dal rhaid gwirio am nodau cyswllt, trychben a chysylltben,
    ac odlau cudd: mae rhain yn symud neu copio nodau ar draws
    bylchau rhwng geiriau (ar ol iddynt gael eu seinegoli os
    oes angen).

    Felly dylen ni *ddim* gwneud copi o'r uned, ond yn hytrach
    Rydym yn storio'r trosiadau yn y nodau unigol, a chael ffwythiannau
    recursive i ddychwelyd yr uned lythrennol neu seinegol
    fel sydd angen. Mae hyn yn golygu nad oes angen cadw map o'r
    trosiadau yn y dadansoddiad (gellir dadlau nad yw'r broses o
    seinegoli yn wir berthyn i'r dadansoddiad anyway)

    nod.text()
    nod.text(seinegol=True)

    Mewnbwn: `uned` sef `Gair`, `Llinell`, `Cwpled` neu `Pennill`
    Allbwn: dim

    Mae'r broses yn delio a cyfresi cytseiniaid o'r dde i'r chwith

    """
    # Copi o'r geiriau gwreiddiol
    # uned = deepcopy(uned)

    # Echdynnu rhestr sillafau
    if type(uned) is Gair:
        sillafau = uned.children

    elif type(uned) is Llinell:
        sillafau = [sillaf for gair in uned.children for sillaf in gair.children]

    elif type(uned) is Pennill:
        sillafau = [gair for llinell in uned.children for gair in llinell.children]

    elif type(uned) in (list, tuple) and all([type(x) is Gair for x in uned]):
        sillafau = [sillaf for gair in uned for sillaf in gair.children]

    elif type(uned) in (list, tuple) and all([type(x) is Sillaf for x in uned]):
        sillafau = uned

    else:
        raise ValueError("Rhaid cael `Gair, `Llinell` neu `Pennill`.")

    # Dadansoddiad er mwyn cario hysbys
    dad = Dadansoddiad()

    # Sillaf wag i ddechrau er mwyn cael prosesu cyrch y gair cyntaf
    sillaf = Sillaf()

    for sillaf, sillaf_nesaf in zip(sillafau[:-1], sillafau[1:]):
        coda = sillaf.coda()
        cyrch_nesaf = sillaf_nesaf.cyrch()

        # log.info("{}. Prosesu sillafau ({}, {})".format(count, sillaf, sillaf_nesaf))
        # log.info("Prosesu (coda, cyrch) = ({}, {})".format(coda, cyrch))

        # Hepgor sillafau llafarog
        if not coda.children and not cyrch_nesaf.children:
            sillaf = sillaf_nesaf
            # print("skip {}, {}".format(coda, cyrch))
            continue

        # prosesu fesul par o gytseiniaid
        cc = coda.children + cyrch_nesaf.children

        for nod1, nod2 in zip(cc[:-1],cc[1:]):

            # cywasgu cytseiniaid ddwbl
            if cywasgu and nod1.text == nod2.text:
                nod2.sain = ''
                msg = f"cywasgu: {(nod1, nod2)} ->  {nod1}"
                dad.hysbys.append(msg)

            # meddalu dan effaith y gytsain flaenorol
            if meddalu and nod2.text.lower() in cyfatebiaeth_meddal:
                if nod1.text.lower() in cytseiniaid_meddalu:
                    nod2.sain = cyfatebiaeth_meddal[nod2.text.lower()]
                    msg = f"meddalu: {nod1.text+nod2.text} -> {nod2.text+nod2.sain}"
                    dad.hysbys.append(msg)

            # caledu
            if caledu and (nod1.text.lower(), nod2.text.lower()) in cyfuniadau_caled:
                cyfuniad = cyfuniadau_caled[nod1.text.lower(), nod2.text.lower()]
                nod1.sain = cyfuniad[0]
                nod2.sain = cyfuniad[1]
                # msg = f"caledu {(nod1.text, nod2.text)} -> {(nod1.sain, nod2.sain)}"
                msg = "caledu: {}+{} -> {}+{}".format(nod1, nod2, nod1.sain, nod2.sain)
                # print('msg = ', msg)
                dad.hysbys.append(msg)

    return dad

# trawslythrennu ac i ag, ap i ab ayb
# def meddalu_ac(uned):
#     pass

def hollti_cyfuniadau_trychben(uned):

    geiriau = uned.geiriau()
    for gair in geiriau:
        coda = gair.children[-1].coda()
        cyts = coda.cytseiniaid()
        if len(cyts) > 1:
            tr = ''.join([c.text for c in cyts[-2:]])
            if tr in cyfuniadau_trychben:
                cytsain_olaf = coda.children.pop()
                cnew = gair.children[-1].cnewyllyn()
                llafariad_newydd = Nod(cnew[-1].text)
                sillaf = Sillaf()
                sillaf.cnewyllyn().children.append(llafariad_newydd)
                sillaf.coda().children.append(cytsain_olaf)
                gair.children.append(sillaf)
                # print(f'Holltwyd gyfuniad trychben: {tr}')

def meddalu_ac(uned):
    '''
    Mae'n llawer haws newid ac -> ag ar lefel geiriau, nid sillafau.
    '''

    geiriau = list(uned.geiriau())  # copy
    if not geiriau:
        return
    geiriau.reverse()

    while geiriau:
        x = geiriau.pop()
        if str(x).lower() not in ['ac',]:
            continue


        # popio'r olynydd
        y = geiriau.pop()

        # check sillaf cyntaf
        if len(y.children) > 0:
            y_sill_cyntaf = y.children[0]  # sillaf
            # print('ysc: ', y_sill_cyntaf)

            # profi am sill gyntaf lafarog
            if y_sill_cyntaf and not y_sill_cyntaf.cyrch().children:

                ycn = y_sill_cyntaf.cnewyllyn()
                # print('ycn: ', cn)

                if len(ycn.children) > 0:

                    # echdynnu'r sill olaf yr 'ac'
                    if len(x.children) > 0:
                                    
                        x_sill_olaf = x.children[0]  # sillaf
                        # print('xso: ', x_sill_olaf)

                        if x_sill_olaf and x_sill_olaf.coda():
                            xco = x_sill_olaf.coda()  # cyfres
                            # print('xco: ', xco)
                            if len(xco) > 0:  # and len(xco.children) > 0:
                                xco.children[-1].sain = 'g'


def seinegoli(uned, cywasgu=True, meddalu=True, caledu=True):

    meddalu_ac(uned)
    # hollti_cyfuniadau_trychben(uned)
    seinegoli_fesul_sillaf(uned, cywasgu=True, meddalu=meddalu, caledu=caledu)


if __name__ == "__main__":

    test_data = [
        "O dad, yn deulu dedwydd",
        "Lle i enaid gael llonydd",
        "Ond daw gwefr cyn atgofion",
        "Y ddinas draw yn wastraff",
        "Yn wyneb haul ar Epynt",
        "Yr esgob biau popeth",
        "Aeth fy nghariad hyd ato",
        "O'r garreg hon daeth eco",
        "I'r esgob pur rhoed popeth",
        "Fy nghariad troaf atat",
        "O'r garreg clywaid eco",
        # "Gwae nid gweniaeth",
        # "Yma bu cydnabod",
    ]
    for s in test_data:
        llinell = Llinell(s)
        print(llinell)
        geiriau = llinell.children
        print("gwreiddiol: {}".format(geiriau))
        dad = seinegoli(llinell)
        # print("trosiadau:  {}".format(dad.trosiadau))
        if dad:
            print(dad.hysbys)
        print('-----')
        # dad = seinegoli(llinell)
        print(llinell.sain())

        print("--------------------")

    s = 'drws y neidr'
    llinell = Llinell(s)
    print(llinell)
    print(llinell.sain())

    uned = Uned(cynnwys=llinell)
    hollti_cyfuniadau_trychben(uned)

    print(llinell.sain())
    
    print('----------')
    s = "Arian ac aur yn ei god"

    llinell = Llinell(s)
    # print(llinell)
    print(llinell.sain())

    uned = Uned(cynnwys=llinell)
    meddalu_ac(uned)

    print(llinell.sain())
 
    # g1 = Gair("wyneb")
    # g2 = Gair("haul")
    # # g1 = Gair("Ond")
    # # g2 = Gair("daw")
    # seinegol, traws = seinegoli(uned=[g1, g2])
    # print(seinegol)
    # print(traws)
