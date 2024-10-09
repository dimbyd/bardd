# odl.py
"""
Dulliau darganfod odl rhwng dau sill

x = x.cyrch|x.cnewyllyn|x.coda + x2.cyrch
y = y.cyrch|y.cnewyllyn|x.coda + y2.cyrch

x = x.a|x.b|x.c   + x2.a
y = y.a|y.b|y.c   + y2.a

odl:    (x.c == y.c) a (x.b == y.b)
proest: (x.c == y.c) a (x.b != y.b) # ond yr un pwysau

# dosbarthiadau = {
#    ('OGY', 'odl gyflawn'),
#    ('OLA', 'odl lafarog'),
#    ('OLU', 'odl lusg'),
#    ('OLL', 'odl lusg lafarog'),
#    ('PGY', 'proest gyflawn'),
#    ('PLA', 'proest lafarog'),
# }
"""

from bardd.cysonion import atalnodau, deuseiniaid, dosbarth_deusain
# from bardd.cyfres import Cyfres
from bardd.sillaf import Sillaf
from bardd.gair import Gair
from bardd.dadansoddiad import Dadansoddiad
from bardd.seineg import seinegoli_fesul_sillaf

import logging
log = logging.getLogger(__name__)


def prawf_odl(x, y, odl_lusg=False, trwm_ac_ysgafn=False):
    """
    input x: `Gair` unigol, neu tuple (`Gair`, `Gair`)
    input y: `Gair` unigol, neu tuple (`Gair`, `Gair`)
    output: dosbarth odl

    odlau cudd: benthyg cytsain/cytseiniaid cyntaf y gair 
    olynol i greu odl
    """

    # init
    dad = Dadansoddiad()

    # Echdynnu'r olynwyr os oes angen
    x_olynydd = None
    if type(x) is tuple and len(x) == 2:
        x_olynydd = x[1]
        x = x[0]
    y_olynydd = None
    if type(y) is tuple and len(y) == 2:
        y_olynydd = y[1]
        y = y[0]

    # type check
    if type(x) is not Gair:
        raise TypeError("Mae angen Gair fan hyn, nid {}".format(type(x)))
    if type(y) is not Gair:
        raise TypeError("Mae angen Gair fan hyn, nid {}".format(type(y)))
    if x_olynydd and type(x_olynydd) is not Gair:
        raise TypeError("Mae angen Gair fan hyn, nid {}".format(type(x_olynydd)))
    if y_olynydd and type(y_olynydd) is not Gair:
        raise TypeError("Mae angen Gair fan hyn, nid {}".format(type(y_olynydd)))

    # Gwirio bod o leiaf un sill bob ochr
    if not x.children or not y.children:
        return dad

    # Echdynnu sill olaf y gair cyntaf
    x_sill_olaf = x.children[-1]

    # Echdynnu sill olaf (neu olaf-ond-un) yr ail air
    if odl_lusg:
        if y.nifer_sillafau() < 2:
            dad.gwallau.append('Odl lusg: mae angen gair acennog yn gyntaf a gair diacen yn ail.')
            return dad
        y_sill_olaf = y.children[-2]  # sill olaf-ond-un

    else:
        y_sill_olaf = y.children[-1]  # sill olaf

    # print(f'de {x_sill_olaf}, {y_sill_olaf}')

    # prawf sylfaenol
    dad = prawf_odl_sylfaenol(x_sill_olaf, y_sill_olaf,
                              odl_lusg=odl_lusg, trwm_ac_ysgafn=trwm_ac_ysgafn)

    # dychwelyd os oes llwyddiant
    if dad.dosbarth in ['OGY', 'OLA', 'OLU', 'OLL']:
        return dad

    # chwilio am gollnod ar y diwedd: a'r, i'm, ayb
    xcn = x_sill_olaf.cnewyllyn().children
    # print('xso = ', x_sill_olaf, '; yso = ', y_sill_olaf, '; xcn = ', xcn)
    # print('xcn[-1].text = ', xcn[-1].text)
    # print(xcn[-1].text in atalnodau)

    # talfyru olddodiad e.e. 'r
    # mae'r atalond wastad ar ddiwedd y cnewyllyn (nid ar ddechrau'r coda)
    # mae "Daw'r" yn odli gyda "nawr" a "glaw"
    if xcn and xcn[-1].text in atalnodau:
        # cnew = x_sill_olaf.cnewyllyn()
        # x_sill_newydd = Sillaf(cnewyllyn=str(cnew[:-1]))
        atalnod = xcn.pop()
        xco = x_sill_olaf.coda()
        xco_kids = xco.children
        xco.children = []
        dad = prawf_odl_sylfaenol(x_sill_olaf, y_sill_olaf,
                                  odl_lusg=odl_lusg,
                                  trwm_ac_ysgafn=trwm_ac_ysgafn)
        xcn.append(atalnod)
        xco.children = xco_kids
        if dad.dosbarth in ['OGY', 'OLA', 'OLU', 'OLL']:
            return dad

    # ailadrodd ar gyfer y
    ycn = y_sill_olaf.cnewyllyn().children
    if ycn and ycn[-1].text in atalnodau:
        atalnod = ycn.pop()
        yco = y_sill_olaf.coda()
        yco_kids = yco.children
        yco.children = []
        # cnew = y_sill_olaf.cnewyllyn()
        # atalnod = ycn.pop()
        # y_sill_newydd = Sillaf(cnewyllyn=str(cnew[:-1]))
        # print('xs_newydd: ', repr(x_sill_newydd))
        # print('ycnew: ', repr(y_sill_olaf.cnewyllyn()))
        dad = prawf_odl_sylfaenol(x_sill_olaf, y_sill_olaf, odl_lusg=odl_lusg, trwm_ac_ysgafn=trwm_ac_ysgafn)
        ycn.append(atalnod)
        yco.children = yco_kids
        if dad.dosbarth in ['OGY', 'OLA', 'OLU', 'OLL']:
            return dad

    # --------------------
    # Chwilio am odlau cudd

    # echdynnu sill cyntaf yr olynydd
    x_olynydd_sill_cyntaf = None
    if x_olynydd and x_olynydd.children:
        x_olynydd_sill_cyntaf = x_olynydd.children[0]
    y_olynydd_sill_cyntaf = None
    if y_olynydd and y_olynydd.children:
        y_olynydd_sill_cyntaf = y_olynydd.children[0]  # sain yn unig

    # print('xolynydd_sill_cyntaf = ', x_olynydd_sill_cyntaf)
    # print('yolynydd_sill_cyntaf = ', y_olynydd_sill_cyntaf)

    # prawf
    def prawf_odl_gudd(xolaf, yolaf, xolynydd=None, yolynydd=None):

        dad = Dadansoddiad()
        if xolynydd:
            xolaf_coda_hyd = len(xolaf.coda().children)
            xolynydd_cyrch_nodau = list(xolynydd.cyrch().cytseiniaid())
            xolynydd_cnew_nodau = list(xolynydd.cnewyllyn().llafariaid())
            xnodau = xolynydd_cyrch_nodau + xolynydd_cnew_nodau
            # print('xnodau = ', xnodau)
            # print('xolynydd_cyrch_nodau = ', xolynydd_cyrch_nodau)
            # print('xolynydd_cnew_nodau = ', xolynydd_cnew_nodau)
            while xnodau:
                xnod = xnodau.pop(0)  # pop o'r blaen
                xolaf.coda().children.append(xnod)

                dad = prawf_odl_sylfaenol(xolaf, yolaf, odl_lusg=odl_lusg)
                if dad.dosbarth in ['OGY', 'OLA', 'OLU', 'OLL']:
                    dad.hysbys = ["odl gudd"]
                    xolaf.coda().children = xolaf.coda().children[:xolaf_coda_hyd]
                    return dad
                
                if yolynydd:
                    yolaf_coda_hyd = len(yolaf.coda().children)
                    yolynydd_cyrch_nodau = list(yolynydd.cyrch().cytseiniaid())
                    yolynydd_cnew_nodau = list(yolynydd.cnewyllyn().llafariaid())
                    ynodau = yolynydd_cyrch_nodau + yolynydd_cnew_nodau
                    # print('ynodau = ', ynodau)
                    while ynodau:
                        ynod = ynodau.pop(0)  # pop o'r blaen
                        yolaf.coda().children.append(ynod)
                        dad = prawf_odl_sylfaenol(xolaf, yolaf, odl_lusg=odl_lusg)

                        if dad.dosbarth in ['OGY', 'OLA', 'OLU', 'OLL']:
                            dad.hysbys = ["odl gudd (ail)"]
                            xolaf.coda().children = xolaf.coda().children[:xolaf_coda_hyd]
                            yolaf.coda().children = yolaf.coda().children[:yolaf_coda_hyd]
                            return dad

                    yolaf.coda().children = yolaf.coda().children[:yolaf_coda_hyd]
            xolaf.coda().children = xolaf.coda().children[:xolaf_coda_hyd]
            return dad

    # prawf am odl gudd
    dad_odl_gudd = prawf_odl_gudd(
        x_sill_olaf,
        y_sill_olaf,
        xolynydd=x_olynydd_sill_cyntaf,
        yolynydd=y_olynydd_sill_cyntaf,
    )
    return dad_odl_gudd


def prawf_odl_sylfaenol(x, y, odl_lusg=False, trwm_ac_ysgafn=False):
    """
    Gwirio am odl sylfaenol rhwng dau `Sillaf`
    Rhaid meddalu, caledu ayb cyn hyn
    """
    # Type check
    if type(x) is not Sillaf or type(y) is not Sillaf:
        raise ValueError("Rhaid i'r mewnbynnau fod o'r math `Sillaf`")

    # init
    dad = Dadansoddiad()
    # dad.nodau = []

    # Echdynnu'r codau (heb atalnodau)
    x_coda = x.coda().cytseiniaid()
    y_coda = y.coda().cytseiniaid()

    # Gwirio os yw'r ddau coda yn cyfateb, yn
    # cynnwys dau linyn gwag (am odl lafarog)
    #
    # Os nad yw'r ddau yn cyfateb, does dim odl.
    #
    # x_coda_str = "".join([nod.text for nod in x_coda])
    # y_coda_str = "".join([nod.text for nod in y_coda])
    x_coda_str = "".join([nod.sain for nod in x_coda])
    y_coda_str = "".join([nod.sain for nod in y_coda])

    # print('xcs = ', x_coda_str, '; ycs = ', y_coda_str)

    if x_coda_str and y_coda_str and x_coda_str != y_coda_str:
        return dad
    if (not x_coda_str and y_coda_str) or (x_coda_str and not y_coda_str):
        return dad

    # Echdynnu'r cnewyll (heb atalnodau)
    x_cnew = x.cnewyllyn().llafariaid()
    y_cnew = y.cnewyllyn().llafariaid()

    # if trwm_ac_ysgafn:
    #     x_cnew = x.cnewyllyn().llafariaid()
    #     y_cnew = y.cnewyllyn().llafariaid()
    # else:
    #     x_cnew = Cyfres([nod.byr() for nod in x.cnewyllyn().llafariaid()])
    #     y_cnew = Cyfres([nod.byr() for nod in y.cnewyllyn().llafariaid()])

    # Talfyrru cnewyll trisain ()
    if len(x_cnew) > 2:
        x_cnew.children = x_cnew.children[-2:]
    if len(y_cnew) > 2:
        y_cnew.children = y_cnew.children[-2:]

    # print('cn ', type(x_cnew), type(y_cnew))

    # Echdynnu'r llinynnau ysgafn cyfatebol
    # ar gyfer darganfod dosbarth deusain (lookups)
    #
    # Mae angen profi os yw'r llafariad yn hir neu yn fyr
    # felly mae'n rhaid cario'r cyfresi nodau x_cnew a y_cnew
    # sy'n cynnwys y llafariad gwreiddiol
    #
    # Does dim angen poeni am ddeugraffau fan hyn
    # gan mai cystseiniaid yw deugraffau bob amser
    #
    x_str = "".join([nod.byr().text for nod in x_cnew])
    y_str = "".join([nod.byr().text for nod in y_cnew])

    # Gwirio os yw'r deuseiniaid yn wybyddus i'r system
    if len(x_str) > 1 and x_str not in dosbarth_deusain:
        dad.hysbys.append('Heb adnobod y ddeusain {}.'.format(x_str))
        return dad
    if len(y_str) > 1 and y_str not in dosbarth_deusain:
        dad.hysbys.append('Heb adnobod y ddeusain {}.'.format(y_str))
        return dad

    # print('xstr = ', x_str, '; ystr = ', y_str)

    # baneri
    odl = False
    proest = False

    # ----------------------
    # 1. dwy lafariad unigol
    if len(x_cnew) == 1 and len(y_cnew) == 1:

        # odl: cnewyll yn cyfateb
        if x_cnew[0].text.lower() == y_cnew[0].text.lower():
            odl = True

        # proest: cnewyll o'r un pwysau
        elif x_cnew[0].is_byr() == y_cnew[0].is_byr():
            proest = True

    # 2. deusain talgron a llafariad unigol
    elif len(x_cnew) > 1 and len(y_cnew) == 1 and x_str in deuseiniaid["talgron"]:

        # odl: ail lafariad y ddeusain yn cyfateb
        if x_cnew[1].byr().text == y_cnew[0].byr().text:
            odl = True

        # proest: ail lafariad y ddeusain o'r un pwysau
        elif x_cnew[1].is_byr() == y_cnew[0].is_byr():
            proest = True

    # 3. llafariad unigol a deusain talgron
    elif len(x_cnew) == 1 and len(y_cnew) > 1 and y_str in deuseiniaid["talgron"]:

        # odl: ail lafariad y ddeusain yn cyfateb
        if x_cnew[0].byr().text == y_cnew[1].byr().text:
            odl = True

        # proest: ail lafariad y ddeusain o'r un pwysau
        elif x_cnew[0].is_byr() == y_cnew[1].is_byr():
            proest = True

    # 4. dwy ddeusain
    elif len(x_cnew) > 1 and len(y_cnew) > 1:

        # odl: cyfatebiaeth union
        if x_cnew[0].text == y_cnew[0].text and x_cnew[1].text == y_cnew[1].text:
            odl = True

        # odl: cyfatebiaeth rhwng dwy ddeusain talgron wahanol
        elif x_str in deuseiniaid["talgron"] and y_str in deuseiniaid["talgron"]:

            # ... os yw'r llafariaid terfynol yn cyfateb
            if x_cnew[1].text == y_cnew[1].text:
                odl = True

        # proest: cyfatebiaeth rhwng dwy ddeusain lleddf wahanol
        elif x_str in deuseiniaid["lleddf"] and y_str in deuseiniaid["lleddf"]:

            # ... a'r ddau o'r un dosbarth
            if dosbarth_deusain[x_str] == dosbarth_deusain[y_str]:
                proest = True

        # end cases

    # print('x_cnewyllyn: ', x_cnewyllyn)
    # print('x_coda: ', x_coda_str)
    # print('y_coda: ', y_coda_str)
    # print('x_cnewyllyn + x_coda: ', type(x_cnewyllyn + x_coda))
    # print(odl)

    # dosbarthu
    if odl:
        if x_coda_str and y_coda_str:
            # print('Hwre2')
            dad.dosbarth = "OGY" if not odl_lusg else "OLU"
        else:
            dad.dosbarth = "OLA" if not odl_lusg else "OLL"
    if proest:
        if x_coda and y_coda:
            dad.dosbarth = "PGY" if not odl_lusg else "PLU"
        else:
            dad.dosbarth = "PLA" if not odl_lusg else "PLL"

    # atodi'r nodau sy'n creu yr odl
    if dad.dosbarth:
        # print('Hwre3')
        dad.nodau = [x_cnew + x_coda, y_cnew + y_coda]
        # print('dad_odl: ', dad)
        return dad

    return dad  # empty


# main
def main():

    from bardd.data_odl import profion

    profion["problem_lusg"] = {
        ("bedw", "dedwydd"),
    }

    for key in [
        "odlau_cyflawn",
        "odlau_llafarog",
        # "proestau_cyflawn",
        # "proestau_llafarog",
        "odlau_llusg",
        "odlau_llusg_cudd",
        # "odlau_llusg_ewinog",
        # "problem_lusg"
    ]:
        print("==============================")
        print(key.upper())
        print("==============================")
        for tup in profion[key]:
            g1 = Gair(tup[0])
            g2 = Gair(tup[1])
            g3 = Gair(tup[2]) if len(tup) > 2 else None

            seinegoli_fesul_sillaf([g1, g2])  # gyda'i gilydd
            # print(g1, g2)
            # print(g1.sain(), '+', g2.sain())
            if g3:
                seinegoli_fesul_sillaf(g3)
                # print(g3.sain())
            if not g3:
                print("{}/{}".format(g1, g2))
            else:
                print("{}+{}/{}".format(g1, g2, g3))
                print("{}+{}/{}".format(g1.sain(), g2.sain(), g3.sain()))


            if key in ["odlau_llusg"]:
                dad = prawf_odl(g1, g2, odl_lusg=True)

            elif key in ["odlau_llusg_cudd", "odlau_llusg_ewinog", "triphlyg"] and g3:
                dad = prawf_odl((g1, g2), g3, odl_lusg=True)

            else:
                dad = prawf_odl(g1, g2)

            # show
            print(dad.beiro.cyan(dad.dosbarth))
            # print(dad.hysbys)
            # print(dad.nodau)
            # print("--------------------")
            # print(dad.adroddiad())
            # for key2 in dad.nodau.keys():
            #     if dad.nodau[key2]:
            #         print("{} : {}".format(key2, repr(dad.nodau[key2])))
            print("--------------------")

        # print("Ad-hoc")
        # # g1 = Gair('sôn')
        # # g2 = Gair('llon')
        # # g1 = Gair('dringo')
        # # g2 = Gair('rhodio')
        # g1 = Gair('canlyniad')
        # g2 = Gair('cariad')
        # g1 = Gair('Rhwydd')
        # g2 = Gair('Hawdd')
        # g1 = Gair('a')
        # g1o = Gair('dy')
        # g2 = Gair('cariad')
        # g1 = Gair("Daw'r")
        # g2 = Gair("glaw")
        g1 = Gair("Gŵr")
        g1 = Gair("Gwr")
        g2 = Gair("morwr")
        dad = prawf_odl(g1, g2, trwm_ac_ysgafn=True)
        print(dad)
        dad = prawf_odl(g1, g2, trwm_ac_ysgafn=False)
        print(dad)
        # dad = prawf_odl((g1, g1o), g2, trwm_ac_ysgafn=False)
        print("{}/{}".format(g1, g2))
        print(dad.beiro.cyan(dad.dosbarth))
        print(dad.adroddiad())

    return


if __name__ == "__main__":
    main()
