"""
cytseinedd.py

Darganfod a dadansoddi cytseinedd

Mae sawl rhestr nodau yn cael eu cofnodi:
nodau = {
    'cyfatebol' = None,
    'gwreiddgoll'     # cytseiniaid blaen
    'traws' = None,   # cytseiniaid ar ddechrau'r ail gymal
    'trychben' = None,
    'cysylltben' = None,
    'diwedd_yrorffwysfa = None,
    'diwedd_ybrifodl = None,
}

Dyma'r hierarchaeth:
    geiriau = [Gair, Gair, Gair]
    Gair = [Sillaf, Sillaf, Sillaf]
    Sillaf = [Cyfres, Cyfres, Cyfres]
    Cyfres = [Nod, Nod, Nod]

"Y llwybrau gynt lle bu'r gan"

.y.|ll.wy.br|.au.|g.y.nt
ll.e.|b.u'.r|g.a.n

Mewnbwn: dau restr geiriau
Allbwn: dosbarth,

[ll, (b,r), g, (n,t)]
[ll, b, r, g, n]

Aceniad
CAC: match x[:-1] and y[:-1]
CDI: match [x:-1] and y[:-1]
ADI: match x with y[:-1]
ADY: match x[:-2] with y[:-1]

Aceniad
CAC: x[-1].cyrch == y[-1].cyrch and x[-1].coda != y[-1].coda
CDI: x[-2].coda + x[-1].cyrch == y[-2].coda + y[-1].cyrch
ADI: x[-1].cyrch + x[-1].coda ==  y[-2].cyrch  + y[-2].coda + y[-1].cyrch
ADY: x[-2].cyrch  + x[-2].coda + x[-1].cyrch == y[-1].cyrch + y[-1].coda

Cyfuniadau trychben
Mae cytsain olaf y rhan gyntaf yn symud ar draws y toriad (tua'r dde)
ac yn cysylltu gyda chytseiniaid blaen yr ail ran

Croes-o-gyswllt: mae posib neidio dros llafariaid terfynnol
e.e. daw geiriau duw | o'i gaer deg

Cyfuniadau cysylltben
Mae cytsain gyntaf yr ail ran yn symud ar draws y toriad
tua'r chwith, ac cysylltu gyda chytseiniaid yr orffwysfa

"""

# from bardd.cyfres import Cyfres

from bardd.cysonion import atalnodau
from bardd.cysonion import cyfuniadau_trychben
from bardd.cysonion import max_cytseiniaid_cyswllt, max_cytseiniaid_pengoll
from bardd.gair import Gair
from bardd.beiro import Beiro

from bardd.seineg import seinegoli_fesul_sillaf

from bardd.cyfres import Cyfres
from bardd.dadansoddiad import Dadansoddiad


def cyfatebiaeth(nod1, nod2):
    """
    Gwirio os yw dau gytsain yn cyfateb.
    Mewnbwn: dau `Nod`
    Allbwn: bool
    """
    # s1 = nod1.text.lower()
    # s2 = nod2.text.lower()
    s1 = nod1.sain.lower()
    s2 = nod2.sain.lower()

    # print('cyf text: ', (nod1.text, nod2.text))
    # print('cyf sain: ', (s1, s2))

    if s1 == s2:
        return True
    elif s1 == "r" and s2 == "rh":
        return True
    elif s1 == "rh" and s2 == "r":
        return True
    elif s1 == "s" and s2 == "sh":
        return True
    elif s1 == "sh" and s2 == "s":
        return True
    elif s1 == "ph" and s2 == "ff":
        return True
    elif s1 == "ff" and s2 == "ph":
        return True
    else:
        return False


def cysefeillio(x_nodau, y_nodau):
    """
    Chwilio am gyfatebiaeth rhwng dau restr cytseiniaid.
    Mae'r broses cysefeillio yn mynd o'r dde i'r chwith.
    Mewnbwn: dau restr cytseiniaid (wedi eu trawsnewid os oes angen)
    Allbwn: tri rhestr nodau
        cyfatebol: rhestr parau (o'r dde i'r chwith)
        x_blaen: gweddill y rhestr cyntaf
        y_blaen: gweddill yr ail restr
    """
    cytseiniaid_cyfatebol = []
    hysbys = []

    x_nodau = list(x_nodau)  # copi
    y_nodau = list(y_nodau)  # copi

    while x_nodau and y_nodau:
        x_nod = x_nodau.pop()
        y_nod = y_nodau.pop()

        if not x_nod.sain:
            y_nodau.append(y_nod)  # trio eto!
            continue

        if not y_nod.sain:
            x_nodau.append(x_nod)  # trio eto!
            continue

        # profi am gyfatebiaeth
        if cyfatebiaeth(x_nod, y_nod):
            cytseiniaid_cyfatebol.append((x_nod, y_nod))

            if x_nodau and y_nodau and not cyfatebiaeth(x_nodau[-1], y_nodau[-1]):

                # dau yn ateb un (rhan flaen)
                if x_nodau and cyfatebiaeth(x_nod, x_nodau[-1]):
                    hysbys.append(f"x: dau yn ateb un: {(x_nod, (x_nod, x_nodau[-1]))}")
                    x_nod = x_nodau.pop()
                    cytseiniaid_cyfatebol.append((x_nod, y_nod))
                    # continue

                # dau yn ateb un (ail ran)
                # print('xxxx = ', (y_nod, y_nodau[-1]))
                # print('xxxx = ', cyfatebiaeth(y_nod, y_nodau[-1]))
                if y_nodau and cyfatebiaeth(y_nod, y_nodau[-1]):
                    hysbys.append(f"y: dau yn ateb un: {(y_nod, (y_nod, y_nodau[-1]))}")
                    y_nod = y_nodau.pop()
                    cytseiniaid_cyfatebol.append((x_nod, y_nod))
                    # continue

        # print(f'(x_nod_sain, y_nod_sain) = ({x_nod.sain},{y_nod.sain})')

        #  h heb ei hateb
        elif x_nod.text in ["h", "H"]:
            y_nodau.append(y_nod)  # trio eto!
            # hysbys.append("h-heb-ei-hateb")

        elif y_nod.text in ["h", "H"]:
            x_nodau.append(x_nod)
            # hysbys.append("h-heb-ei-hateb")

        # dim cyfatebiaeth
        else:
            x_nodau.append(x_nod)  # ailosod
            y_nodau.append(y_nod)
            break

    cytseiniaid_cyfatebol.reverse()
    return (cytseiniaid_cyfatebol, x_nodau, y_nodau, hysbys)


def aceniad(x_geiriau, y_geiriau):
    """
    Dosbarthu dwy gyfres geiriau yn ol aceniad.
    Mewnbwn: dau restr `Gair`
    Allwbwn: llinyn ddosbarth
    """
    if x_geiriau[-1].acennog() and y_geiriau[-1].acennog():
        return "CAC"  # cytbwys acennog

    elif x_geiriau[-1].acennog() and not y_geiriau[-1].acennog():
        return "ADI"  # anghytbwys ddiacen (disgynedig)

    elif not x_geiriau[-1].acennog() and y_geiriau[-1].acennog():
        return "AAC"  # anghytbwys acennog (dyrchafedig)

    else:
        return "CDI"  # cytbwys ddiacen


def traeannu(geiriau):
    """
    Mewnbwn:
        Rhestr gwrthrychau `Gair`
    Allbwn:
        Tri rhestr nodau: blaen, canol, diwedd

    Y canol yw "dan yr acen"
    """

    # type check
    if type(geiriau) is Gair:
        geiriau = list(geiriau)

    # creu rhestr sillau
    sillafau = [sill for gair in geiriau for sill in gair.children]
    # print('sillafau: {}'.format(sillafau))
    if not sillafau:
        return [], [], []

    # dechrau
    sill_olaf = sillafau.pop()

    # 1. diwedd acennog (unsill neu lluosill acennog)
    if geiriau and geiriau[-1].acennog():
        cyrch_nesaf = sill_olaf.cyrch()
        canol = sill_olaf.coda().cytseiniaid()  # sef dan yr acen
        diwedd = []

    # diwedd ddiacen (lluosill bob tro)
    elif geiriau and sillafau:
        sill_olaf_ond_un = sillafau.pop()
        cyrch_nesaf = sill_olaf_ond_un.cyrch()
        canol = sill_olaf_ond_un.coda().cytseiniaid() + sill_olaf.cyrch().cytseiniaid()
        diwedd = sill_olaf.coda().cytseiniaid()

    else:
        cyrch_nesaf = Cyfres()  # hack
        canol = []
        diwedd = []

    # echdynnu cytseiniaid y rhan flaen
    blaen = Cyfres()
    while sillafau:
        sillaf = sillafau.pop()
        cc = sillaf.coda().cytseiniaid() + cyrch_nesaf.cytseiniaid()
        blaen = cc + blaen
        cyrch_nesaf = sillaf.cyrch()

    if cyrch_nesaf:
        blaen = cyrch_nesaf.cytseiniaid() + blaen

    # diwedd
    return blaen, canol, diwedd


def prawf_cytseinedd_sylfaenol(x_geiriau, y_geiriau):
    """
    Darganfod patrwm cytseinedd.
        - Cysefeillio cytseiniaid blaen
        - Cysefeillio cytseiniaid canol (os oes angen)
    """

    x_geiriau = list(x_geiriau)  # copy
    y_geiriau = list(y_geiriau)  # copy

    # init dadansoddiad
    dad = Dadansoddiad()
    dad.nodau = {}  # dict am y dosbyrth cytseiniaid

    # dadelfeniad
    x_blaen, x_canol, x_diwedd = traeannu(x_geiriau)
    y_blaen, y_canol, y_diwedd = traeannu(y_geiriau)

    # print('xb, xc, xd = ', (x_blaen, x_canol, x_diwedd))
    # print('yb, yc, yd = ', (y_blaen, y_canol, y_diwedd))

    # 1. Profi bod cytseiniaid olaf cyfuniadau cytbwys acennog (CAC) yn wahanol
    if x_geiriau[-1].acennog() and y_geiriau[-1].acennog():
        # Cytbwys acennog: mae angen i'r cytseiniaid dan yr acen fod yn wahanol
        # print('CAC: ', x_canol, y_canol)
        if x_canol and y_canol and str(x_canol) == str(y_canol):
            # print('bingo')
            dad.dosbarth = 'GWA'
            dad.gwallau.append(f'Proest: {x_geiriau[-1]}, {y_geiriau[-1]}')
            return dad

        cc_canol = []

    # 2 Cytbwys ddiacen (CDI)
    elif not x_geiriau[-1].acennog() and not y_geiriau[-1].acennog():

        # mae angen i'r cytseiniaid olaf fod yn wahanol
        if x_diwedd and y_diwedd and x_diwedd == y_diwedd:
            # dad.dosbarth = 'GWA'
            dad.gwallau.append(f'Proest: dylai\'r cytseiniaid olaf fod yn wahanol: ({x_geiriau[-1]}, {y_geiriau[-1]})')
            return dad
        
        # mae angen cyfatebiaeth union dan yr acen
        cc_canol, xb, yb, hysb = cysefeillio(x_canol, y_canol)
        if xb or yb:
            # dad.dosbarth = 'GWA'
            # print('(xb, yb): ', (xb, yb))
            dad.gwallau.append(f"Dim cyfatebiaeth dan yr acen: ({x_geiriau[-1]}, {y_geiriau[-1]})")
            return dad

    # 3. Anghytbwys ddiacen (ADI)
    # Mae angen cyfatebiaeth union dan yr acen
    # Mae hyn cynnwys sillau llafarog (rhaid i'r ddau ran fod heb gytseiniaid)
    elif x_geiriau[-1].acennog() and not y_geiriau[-1].acennog():
        
        # mae angen cyfatebiaeth union dan yr acen
        cc_canol, xb, yb, hysb = cysefeillio(x_canol, y_canol)
        if xb or yb:
            # print('**(xb, yb): ', (xb, yb))
            dad.gwallau.append("Dim cyfatebiaeth dan yr acen.")
            return dad

    # 4. Anghytbwys acennog (AAC)
    # Does dim rhaid ateb cytseinaid dan yr acen mewn
    # cynghanedd sain anghytbwys acennog. Rhaid peidio
    # gorfodi cyfatebiaethh dan yr acen, mae'n well hidlo
    # canlyniadau anghytbwys acennog nes ymlaen
    else:
        cc_canol = []

    # 3. Profi cytseiniaid y rhannau blaen
    cc_blaen, x_blaen, y_blaen, hysb = cysefeillio(x_blaen, y_blaen)
    dad.hysbys.extend(hysb)

    # cyfuno cytseiniaid y blaen a'r canol
    cc = cc_blaen + cc_canol

    # print('cc = ', cc)
    # print('xb = ', x_blaen)
    # print('yb = ', y_blaen)

    # dosbarthu
    dad = Dadansoddiad()

    # 1. croes (cyfatebiaeth union)
    if cc and not x_blaen and not y_blaen:
        dad.dosbarth = "CRO"

    # 2. croes bengoll
    elif cc and x_blaen and not y_blaen:

        if len(x_blaen) == 1 and x_blaen[0].text.lower() == "n":
            dad.dosbarth = "CRO"
            dad.hysbys.append("n-wreiddgoll")
        elif len(x_blaen):
            dad.dosbarth = 'CBG'

    # 3. traws
    elif cc and not x_blaen and y_blaen:

        # n-ganolgoll
        if len(y_blaen) == 1 and y_blaen[0].text.lower() == "n":
            dad.dosbarth = "CRO"
            dad.hysbys.append("n-ganolgoll")
        else:
            dad.dosbarth = "TRA"

    # 4. traws bengoll
    elif cc and x_blaen and y_blaen:
        if len(x_blaen) == 1 and x_blaen[0].text.lower() == "n":
            dad.dosbarth = "TRA"
            dad.hysbys.append("n-wreiddgoll")
        else:
            dad.dosbarth = "TBG"

    # fel arall mae popeth yn llafarog
    else:
        dad.dosbarth = 'LLA'
        pass

    dad2 = dosbarth_cytseinedd(cc, x_blaen, y_blaen)
    # print('dad2 = ', dad2)
    if dad2 and dad2.dosbarth:
        dad.dosbarth = dad2.dosbarth  # pennu'r dosbarth cytseinedd
        if dad2.hysbys:
            dad.hysbys.extend(dad2.hysbys)

    dad.nodau['cyfateb'] = cc
    if x_blaen:
        dad.nodau['pengoll'] = x_blaen
    if y_blaen:
        dad.nodau['traws'] = y_blaen

    # print('dad = ', dad)

    return dad


def prawf_cytseinedd(x_geiriau, y_geiriau):
    """
    Profi cytseinedd sylfaenol, yna chwilio am
    gytseinedd gyswllt, drychben neu gysylltben
    os oes angen.
    """

    # type check
    if not x_geiriau or not y_geiriau:
        return None
    if type(x_geiriau) is Gair:
        x_geiriau = [x_geiriau]
    if type(y_geiriau) is Gair:
        y_geiriau = [y_geiriau]

    # print('(x,y) = ', (x_geiriau, y_geiriau))


    # prawf sylfaenol
    dad = prawf_cytseinedd_sylfaenol(x_geiriau, y_geiriau)

    # dianc os llwyddiant
    if dad.dosbarth and dad.dosbarth not in ['LLA', 'CBG', 'TBG']:
        # print('fan hyn ', str(dad.gwallau))
        return dad

    # profi am gytesinedd gyswllt, drychben neu gysylltben
    elif x_geiriau and x_geiriau[-1].children and y_geiriau and y_geiriau[0].children:

        # ----------
        # 1. Cytseinedd o Gyswllt
        x_cyts = [c for g in x_geiriau for c in g.cytseiniaid()]  # cytseiniaid y rhan gyntaf
        x_cyts.reverse()
        # print(x_cyts)

        # cwtogi
        x_cyts = x_cyts[:max_cytseiniaid_cyswllt]

        x_sill_olaf = x_geiriau[-1].children[-1]
        y_sill_cyntaf = y_geiriau[0].children[0]
        y_cyrch_hyd = len(y_sill_cyntaf.cyrch().children)  # er mwyn gallu adfer y cyrch gwreiddiol

        # Atodi cytseiniaid diwedd y rhan gyntaf at ddechrau'r ail ran, fesul un.
        for xc in x_cyts:  # o'r dde i'r chwith

            # atodi'r gytsain nesaf i ddechrau'r ail ran
            y_sill_cyntaf.cyrch().children.insert(0, xc)

            # print(f'x_geiriau = {x_geiriau}')
            # print(f'y_geiriau = {y_geiriau}')

            # chwilio eto 
            dad2 = prawf_cytseinedd_sylfaenol(x_geiriau, y_geiriau)

            # dosbarthu
            # if dad2.dosbarth in ['CRO', 'CBG']:
            if dad2.dosbarth == "CRO":

                if y_cyrch_hyd == 0:
                    nodau_cyswllt = y_sill_cyntaf.children[0].children
                    y_sill_cyntaf.cyrch().children = []
                else:
                    nodau_cyswllt = y_sill_cyntaf.children[0].children[:y_cyrch_hyd]
                    y_sill_cyntaf.cyrch().children = y_sill_cyntaf.cyrch().children[-y_cyrch_hyd:]

                dad.dosbarth = "COG"
                dad.nodau = dad2.nodau
                dad.gwallau = dad2.gwallau
                dad.nodau['cyswllt'] = nodau_cyswllt
                return dad

        # ailosod
        if y_cyrch_hyd == 0:
            y_sill_cyntaf.cyrch().children = []
        else:
            y_sill_cyntaf.cyrch().children = y_sill_cyntaf.cyrch().children[-y_cyrch_hyd:]

        # ----------
        # 2. Cytseinedd Drychben
        # Os yw x-blaen yn anwag, profi am gyfuniadau trychben
        # ar ddiwedd gair acennog cyn yr orffwysfa (dan yr acen)
        # Mae ail gytsain y cyfuniad yn croesi'r orffwysfa o'r
        # chwith i'r dde, a'i gynnwys yn rhestr cytseiniaid yr ail ran.
        # e.e. Canu mydr | cyn ymadael
        # print('TRYCHBEN')
        # print(x_geiriau)
        # print(y_geiriau)

        xcc = x_sill_olaf.coda().children
        ycc = y_sill_cyntaf.cyrch().children
        # print('(xcc, ycc)', (xcc, ycc))

        # profi am atalnod ar ddiwedd y coda
        atalnod = None
        if len(xcc) > 2 and xcc[-1].text in atalnodau:
            atalnod = xcc.pop()

        if len(xcc) > 1:
            tr = "".join([nod.sain for nod in xcc[-2:]])
            # print('tr = ', tr)
            # print('xcc = ', xcc)
            if tr in cyfuniadau_trychben:
                nod = xcc.pop()
                ycc.insert(0, nod)

                # print('(xcc, ycc)', (xcc, ycc))
                dad2 = prawf_cytseinedd_sylfaenol(x_geiriau, y_geiriau)
                # print('(xcc, ycc)', (xcc, ycc))

                # ailosod
                nod = ycc.pop(0)
                xcc.append(nod)
                if atalnod:
                    xcc.append(atalnod)


                # dosbarthu
                if dad2.dosbarth in ['CRO', 'COG', 'TRA']:
                    dad = dad2
                    dad.dosbarth = dad.dosbarth[:2] + 'D'
                    dad.nodau['trychben'] = [nod]
                    return dad

        # ----------
        # 3. Cytseinedd Gysylltben
        # Mae angen copio, nid symud, cytsain gyntaf yr ail
        # ran i ddiwedd y rhan gyntaf, er mwyn peidio colli
        # cyfatebiaeth posib gyda chytsain gyntaf y rhan gyntaf
        # e.e. Onid bro | dy baradwys
        # print('CYSYLLTBEN')
        # ycc = y_sill_cyntaf.cyrch().cytseiniaid().children
        # print('(xcc, ycc)', (xcc, ycc))
        if len(ycc) > 0:
            
            nod = ycc[0]  # nid pop
            xcc.append(nod)

            # print('(xcc, ycc)', (xcc, ycc))
            dad2 = prawf_cytseinedd_sylfaenol(x_geiriau, y_geiriau)
            
            # ailosod
            nod = xcc.pop()
            # ycc.insert(0, nod)
            # print('(xcc, ycc)', (xcc, ycc))
            
            if dad2.dosbarth in ['CRO', 'COG', 'TRA']:
                dad = dad2
                dad.dosbarth = dad.dosbarth[:2] + 'G'
                dad.nodau['cysylltben'] = [nod]
                return dad

        # print('diwedd')

    return dad


def dosbarth_cytseinedd(cytseiniaid_cyfatebol, x_blaen, y_blaen):
    """
    Dosbarthu'r cytseinedd e.g. CRO, COG, TRA ayb
    """

    dad = Dadansoddiad()

    # 1. croes (cyfatebiaeth union)
    if cytseiniaid_cyfatebol and not x_blaen and not y_blaen:
        dad.dosbarth = "CRO"

    # 2. croes bengoll
    elif cytseiniaid_cyfatebol and x_blaen and not y_blaen:

        if len(x_blaen) == 1 and x_blaen[0].text.lower() == "n":
            dad.dosbarth = "CRO"
            dad.hysbys.append("n-wreiddgoll")
        
        elif len(x_blaen) <= max_cytseiniaid_pengoll:
            dad.dosbarth = 'CBG'
             

    # 3. traws
    elif cytseiniaid_cyfatebol and not x_blaen and y_blaen:

        # n-ganolgoll
        if len(y_blaen) == 1 and y_blaen[0].text.lower() == "n":
            dad.dosbarth = "CRO"
            dad.hysbys.append("n-ganolgoll")
        else:
            dad.dosbarth = "TRA"

    # 4. traws bengoll
    elif cytseiniaid_cyfatebol and x_blaen and y_blaen:
        if len(x_blaen) == 1 and x_blaen[0].text.lower() == "n":
            dad.dosbarth = "TRA"
            dad.hysbys.append("n-wreiddgoll")
        else:
            dad.dosbarth = "TBG"

    # fel arall mae popeth yn llafarog
    else:
        dad.dosbarth = 'LLA'
        pass

    return dad


# main
def main():

    from bardd.data_cytseinedd import profion
    beiro = Beiro()

    for key in [
        # "croes",
        # "traws",
        # "traws_fantach",
        # "croes_o_gyswllt",
        # "trychben",
        # "cysylltben",
        "caledu",
        "meddalu",
        # "dau-yn-ateb-un",
        # "croes_o_gyswllt_ewinog",
    ]:
        print("\n------------------------------")
        print(key.upper())

        geiriau = profion[key]
        for s1, s2 in geiriau:
            x_geiriau = [Gair(s) for s in s1.split(" ")]
            y_geiriau = [Gair(s) for s in s2.split(" ")]
            s_acenion = (
                " ".join([g.llinyn_acenion() for g in x_geiriau])
                + "   "
                + " ".join([g.llinyn_acenion() for g in y_geiriau])
            )
            s_cytseiniaid = (
                " ".join([g.llinyn_cytseiniaid() for g in x_geiriau])
                + " | "
                + " ".join([g.llinyn_cytseiniaid() for g in y_geiriau])
            )

            print("------------------------------")
            print(s_acenion)
            print("{} | {}".format(s1, s2))
            print(s_cytseiniaid)

            seinegoli_fesul_sillaf(x_geiriau + y_geiriau)

            print('x_geiriau: {}'.format(x_geiriau))
            print('y_geiriau: {}'.format(y_geiriau))

            dad = prawf_cytseinedd(x_geiriau, y_geiriau)

            print('---')
            if dad.dosbarth:
                print(beiro.gwyrdd(dad.dosbarth))
            else:
                print(beiro.coch('DIM'))
            print(dad)

        print("------------------------------")

        print("Ad-hoc")
        # # g1 = Gair('sôn')
        # # g2 = Gair('llon')
        # # g1 = Gair('dringo')
        # # g2 = Gair('rhodio')
        # g1 = Gair('myd')
        # g2 = Gair('mwyn')
        # g1 = Gair('deucant')
        # g2 = Gair('odidocaf')
        # g1 = Gair('gwin')
        # g2 = Gair('gawn')
        x = [Gair(s) for s in 'gennyf dras'.split()]
        y = [Gair(s) for s in 'y dref'.split()]
        dad = prawf_cytseinedd(x, y)
        print("{}/{}".format(x, y))
        # dad = odl(g1, g2, trwm_ac_ysgafn=True)
        # dad = prawf_cytseinedd(g1, g2)
        # print("{}/{}".format(g1, g2))
        print(beiro.cyan(dad.dosbarth))
        print(dad)
        print(dad.gwallau)


if __name__ == "__main__":
    main()
