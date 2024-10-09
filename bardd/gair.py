# gair
"""
Gair: rhestr sillafau
"""

import re
import unidecode

from bardd.base import TreeNode
from bardd.sillaf import Sillaf

from bardd.cysonion import (
    llafariaid,
    llafariaid_hir,
    cytseiniaid,
    atalnodau,
    deuseiniaid,
    dosbarth_deusain,
    eithriadau,
)

import logging
log = logging.getLogger(__name__)

deusain_ddeusill = eithriadau['deusain_ddeusill']


class Gair(TreeNode):
    """
    Dosbarth sy'n mynegi gair fel rhestr sillafau.
    """

    def __init__(self, s=None, parent=None, trychben=False):
        TreeNode.__init__(self, parent=parent)

        if not s:
            return

        if not type(s) is str:
            raise TypeError(
                "Mae angen llinyn fel mewnbwn, nid {}".format(type(s))
            )

        # profi am fylchau
        s = s.strip()
        if re.search(r"\s", s):
            raise ValueError(
                f"Wedi methu creu `Gair` o'r llinyn {s} (bwlch yn bresennol)"
            )

        # profi am linyn gwag
        if not s:
            raise ValueError("Wedi methu creu `Gair` o linyn gwag.")

        # trawsnewid y llinyn i restr sillafau
        idx = 0

        cyrch_nesaf = ""  # hac er mwyn darganfod w-gytsain ar y dechrau

        while idx < len(s):
            cyrch = cyrch_nesaf
            cyrch_nesaf = ""
            while idx < len(s) and not s[idx] in llafariaid:
                cyrch = cyrch + s[idx]
                idx = idx + 1

            cnewyllyn = ""
            while idx < len(s) and not s[idx] in cytseiniaid:
                cnewyllyn = cnewyllyn + s[idx]
                idx = idx + 1

            coda = ""
            while idx < len(s) and not s[idx] in llafariaid:
                coda = coda + s[idx]
                idx = idx + 1

            # creu
            sillaf1 = Sillaf(cyrch, cnewyllyn, coda, parent=self)
            sillaf2 = None

            #
            # Gwirio os oes angen hollti'r cnewyllyn
            # e.e. pan mae deusain deusill (duon)

            # Echdynnu llinyn y cnewyllyn, ond heb atalnodau,
            # er mwyn cael gwirio deuseiniaid
            cnewyllyn = ''.join(
                [c for c in list(cnewyllyn) if c not in atalnodau]
            )

            # anwybyddu atalnodau pur
            if len(cnewyllyn) == 0:
                pass

            # cnewyllyn unsain
            elif len(cnewyllyn) == 1:

                # # edrych am w-gytsain
                # if idx < len(s) - 1 and cnewyllyn in ["w", "W"]:
                #     if cyrch in ["", "g", "G"] and coda in ["l", "n", "r"]:
                #         cyrch_nesaf = cyrch + cnewyllyn + coda
                #         continue
                pass

            # cnewyllyn ddeusain
            elif len(cnewyllyn) == 2:
                if cnewyllyn in deuseiniaid["deusill"]:
                    sillaf1 = Sillaf(cyrch, cnewyllyn[0], "", parent=self)
                    sillaf2 = Sillaf("", cnewyllyn[1], coda, parent=self)
                else:
                    pass

            # cnewyllyn trisain
            elif len(cnewyllyn) == 3:
                # print('cnewyllyn trisain: ', cnewyllyn)
                # print('T: ', deuseiniaid['talgron'])
                # print('LL: ', deuseiniaid['lleddf'])

                # echdynnu deuseiniaid
                cnew = unidecode.unidecode(cnewyllyn)  # ascii
                ds1 = cnew[:2].lower()  # y ddeusain gyntaf
                ds2 = cnew[1:].lower()  # yr ail ddeusain
                # print('(ds1, ds2) = ', (ds1, ds2))

                # check
                if ds1 not in dosbarth_deusain:
                    print("Heb adnabod y ddeusain {}".format(ds1))
                    continue
                if ds2 not in dosbarth_deusain:
                    print("Heb adnabod y ddeusain {}".format(ds2))
                    continue

                if ds1 in deuseiniaid["lleddf"]:

                    # lleddf + lleddf
                    if ds2 in deuseiniaid["lleddf"]:
                        # print('trisain: LL+LL')
                        sillaf1 = Sillaf(cyrch, cnewyllyn[:2], "", parent=self)
                        sillaf2 = Sillaf("", cnewyllyn[2], coda, parent=self)

                    # lleddf + talgron
                    else:
                        # print('trisain: LL+T')
                        sillaf1 = Sillaf(cyrch, cnewyllyn[:2], "", parent=self)
                        sillaf2 = Sillaf("", cnewyllyn[2], coda, parent=self)

                if ds1 in deuseiniaid["talgron"]:

                    # talgron + talgron
                    if ds2 in deuseiniaid["talgron"] and cnew[1] == "w":
                        # print('trisain: T+T')
                        sillaf1 = Sillaf(cyrch, cnewyllyn[:2], "", parent=self)
                        sillaf2 = Sillaf("", cnewyllyn[2], coda, parent=self)

                    # talgron + lleddf e.e. iai = gweddiaid, iwy = bwriwyd
                    else:
                        pass

            # 4. cnewyllyn bedwarsain
            elif len(cnewyllyn) == 4:
                sillaf1 = Sillaf(cyrch, cnewyllyn[:2], "", parent=self)
                sillaf2 = Sillaf("", cnewyllyn[2:], coda, parent=self)

            # 5. cnewyllyn bumsain+
            else:
                log.info("Pump llafariad mewn rhes - oes engrhraifft o hyn?")
                continue

            # atodi'r sillaf/sillafau i'r rhestr
            self.children.append(sillaf1)
            if sillaf2:
                self.children.append(sillaf2)

        # profi am eithriadau (hac)
        if str(self) in eithriadau['deusain_ddeusill']:
            for idx, sillaf in enumerate(self.children):
                cnew = str(sillaf.cnewyllyn())
                if str(cnew) in ['io']:
                    cyrch = str(sillaf.cyrch())
                    coda = str(sillaf.coda())
                    sillaf1 = Sillaf(cyrch, cnew[0], "", parent=self)
                    sillaf2 = Sillaf("", cnew[1], coda, parent=self)
                    self.children = self.children[:idx - 1] + [sillaf1, sillaf2] + self.children[idx + 1:]
                    break

    # priodweddau
    def __str__(self):
        return "".join([str(sillaf) for sillaf in self.children])

    def __repr__(self):
        return "|".join([repr(sillaf) for sillaf in self.children])

    def sain(self):
        return "".join([sillaf.sain() for sillaf in self.children])

    def nodau(self):
        return [
            nod
            for sillaf in self.children
            for cyfres in sillaf.children
            for nod in cyfres.children
        ]

    def llafariaid(self):
        return [nod for nod in self.nodau() if nod.is_llafariad()]

    def cytseiniaid(self):
        return [nod for nod in self.nodau() if nod.is_cytsain()]

    def llythrennau(self):
        return [nod for nod in self.nodau() if nod.is_cytsain or nod.is_llafariad()]

    def nifer_sillafau(self):
        # return len([sillaf for sillaf in self.children if sillaf.cnewyllyn().children])
        return len([sillaf for sillaf in self.children if sillaf.cnewyllyn()])

    def nifer_llafariaid(self):
        return len(self.llafariaid())

    def acennog(self):

        # Geiriau unsill
        if self.nifer_sillafau() == 1:
            return True

        # Gwirio am lafariad byr echblyg ar
        # ddiwedd cnewyllyn y sill olaf
        if self.children:
            cn = self.children[-1].cnewyllyn()
            if cn.children and str(cn.children[-1]) in llafariaid_hir:
                return True

        # Gwirio am h neu rh o flaen y llafariaid olaf
        # e.e. dyfalbarhau ...
        if self.children and len(self.children) > 1:
            if str(self.children[-2].coda()) in ["h", "rh"]:
                return True

        # Gwirio'r rhestr eithriadau
        s = "".join(
            [nod.text.lower() for nod in self.nodau() if nod.text not in atalnodau]
        )
        if s.lower() in eithriadau["lluosill_acennog"]:
            return True

        # diofyn: mae geiriau lluosill yn ddiacen fel arfer
        return False

    def prif_lafariaid(self):
        return tuple([sillaf.prif_lafariad() for sillaf in self.children])

    def prif_lafariad(self):
        prif_laf = self.prif_lafariaid()
        if self.acennog() or self.nifer_llafariaid() == 0:
            return prif_laf[-1]
        return prif_laf[-2]

    # allbwn
    def llinyn_acenion(self, colon=False, blanksymbol=" "):
        ss = list()
        for sillaf in self.children:
            for cyfres in sillaf.children:
                for nod in cyfres.children:
                    if nod is self.prif_lafariad():
                        ss.append("/" if not colon else ":")
                    elif nod in self.prif_lafariaid():
                        ss.append("v" if not colon else ":")
                    else:
                        ss.append(blanksymbol * len(nod.text))
        return "".join(ss)

    def llinyn_llafariaid(self, blanksymbol=" "):
        ss = list()
        for sillaf in self.children:
            for cyfres in sillaf.children:
                for nod in cyfres.children:
                    if nod.is_llafariad():
                        ss.append(nod.text)
                    else:
                        ss.append(blanksymbol * len(nod.text))
        return "".join(ss)

    def llinyn_cytseiniaid(self, blanksymbol=" "):
        ss = list()
        for sillaf in self.children:
            for cyfres in sillaf.children:
                for nod in cyfres.children:
                    if nod.is_cytsain():
                        ss.append(nod.text)
                    else:
                        ss.append(blanksymbol * len(nod.text))
        return "".join(ss)


def main():
    test_data = (
        # cyffredin
        "prydferth",
        "dramodydd",
        "anifeiliaid",
        "cuddio",
        "rhôm",
        "â'th",
        # deuseiniaid
        "dedwydd",
        "ymadael",
        "yw",
        # deusain ddeusill
        "duon",
        "eos",
        "suo",
        # lluosill acennog
        "cymraeg",
        "cangarŵ",
        "ffarwél",
        "dyfalbarhau",
        "dyfalbarhad",
        # w-gytsain
        "awen",
        "llawen",
        "bywyd",
        # w-gytsain yn olaf
        "berw",
        "pitw",
        # w-gytsain gwr, gwl
        "gwaith",
        "gwledd",
        "wledd",
        "gwrandawiad",
        "wrandawiad",
        "gwrando",
        "gwr",
        "gwroldeb",
        "gwrhydri",
        "gŵr",
        "gwrthod",
        # w-gytsain ar y diwedd
        "berw",
        "bedw",
        "llw",
        "pitw",  # eithriad
        # triawd talgron-talgron (T-T)
        "haleliwia",
        "anifeiliaid",
        "piwis",
        "gwiw",
        # triawd talgron-lleddf (T-LL)
        "iaith",
        "gwaith",
        "genwair",
        "gweddiaid", 
        "bwriwyd",
        # triawd lleddf-talgron (LL-T)
        "awen",
        "distewi",
        "gwiw",
        "wiw",
        "piwis",
        "distewi",
        # triawd lleddf-lleddf (LL-LL)
        "gloyw",
        "gwrandawiad",
        "glawio",
        "gloywi",
        # pedwarawd
        "ieuanc",
        # amrywiol
        "daear",  # tri
        "ffiniau",
        # trychben
        "arogl",
        # misc
        "Awdur",
        "2",
    )

    # test_data = ('hyfryd',)

    for s in test_data:
        g = Gair(s, trychben=True)
        print("-------------------")
        print(s.upper())
        print(g.llinyn_acenion())
        print(g)
        print(repr(g))
        print("Nifer sillafau: {}".format(g.nifer_sillafau()))
        # print("Nodau: {}".format(g.nodau()))
        # print("Llafariaid: {}".format(g.llafariaid()))
        # print("Cytseiniad: {}".format(g.cytseiniaid()))
        # print(g.llinyn_acenion(colon=True))
        # print(g.llinyn_llafariaid())
        # print(g.llinyn_cytseiniaid())


if __name__ == "__main__":
    main()
