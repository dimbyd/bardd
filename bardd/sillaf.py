# sillaf.py
"""
Sillafau

Mae tair rhan i bob sillaf: y cyrch (onset), y cnewyllyn (nucleus) a'r coda.

Sillaf = [cyrch, cnewyllyn, coda]

cyrch       `Cyfres` cytseiniaid
cnewyllyn   `Cyfres` llafariaid
cyrch       `Cyfres` cytseiniaid

Sillaf agored (open syllable): dim coda (e.e. pla, glo)
Sillaf gaeëdig (closed syllable): coda yn bresennol (e.e. bwyd, siop)

Acennu deuseiniaid
(1) deuseiniaid lleddf (falling or descending diphthong)
    acen ar y llafariad cyntaf

(2) deuseiniaid talgron (rising or ascending diphthong)
    acen ar yr ail lafariad (dim ond yr ail sydd angen odli)

LL1 = ['aw', 'ew', 'iw', 'ow', 'uw', 'yw'],
LL2 = ['ae', 'ai', 'ei', 'oe', 'oi', 'Wy'],
LL3 = ['au', 'eu', 'ou', 'ey', 'oy'],
T = ['ia', 'ie', 'io',  'iw', 'iy', 'ua', 'wa', 'we', 'wi', 'wo',  'wy', 'yu'],

1. Cnewyllyn sengl
Mae angen gwirio am w-gytsain fan hyn
gwr.a.nd|.o.
gwl.a.d

2. Cnewyllyn ddeusain
d.e.d|.wy.dd
.y.ml|.e.d|.ia.d

Mae hefyd angen hollti deuseiniaid deusill ('uo', 'eo', 'ea', 'oa', 'ee')
d.uo.n -> d.u.|.o.n
.eo.s -> .e.|.o.s
cr.ea.d -> cr.e.|.a.d
d.ee.ll|.i.r -> d.e.|.e.ll|.i.r

3. Cnewyllyn deirsain
Dim ond y ddau lafariad olaf sydd angen cyfateb mewn odl
    e.e. pren/awen (LL-T), iaith/gwaith (T-LL)

3a. Lleddf/Lleddf (LL-LL)
Mewn cyfuniad o dri: aew, oew, auw, euw, ouw, eyw, oyw, ywy
gl.oyw. -> gl.oy.|.w.
d.aea.r => d.ae..a.r
b.ywy.d -> b.yw.|.y.d
cr.e.d|.oau. -> cr.e.d|.o.|.au.

3b. Lleddf/Talgron (LL-T)
Dwy lafariaid cryf naill ochr, llafariad cymharol wan yn y canol
  => Mae ANGEN hollti fan hyn
  => Acenion ar y llafariaid cyntaf ac olaf
.awe.n -> .aw.|.e.n
ll.awe.n -> ll.aw.|.e.n
b.ywy.d -> b.yw.|.y.d

3c. Talgron/Lleddf (T-LL)
Dwy lafariaid cymharol wan naill ochr, llafariad gref yn y canol
  => Does DIM ANGEN hollti fan hyn
  => Acen ar y llafariad ganol (T ac LL yn atgyfnerthu eu gilydd)
g.wai.r
g.e.n|.wai.r
.iai.th
g.wai.th

3d. Talgron - Talgron (T-T)
(i) wiw, wyw - does DIM ANGEN hollti (acen ar y llafariad ganol)
g.wiw.
(ii) iwi, iwy - mae ANGEN hollti (tebyg i LL-T dwy sill)
p.iwi.s -> p.iw.|.i.s
d.iwy.d -> d.i.|.wy.d

(4) Cnewyllyn bedairsain
Mae angen hollti cyfresi o bedwar llafariad mewn i ddau hanner
Dim ond yr ail ddeusain sy'n bwysig mewn odl
.ieua.nc -> .ie.|.ua.nc,
g.wywo -> g.wy.|.wo.
gl.awio. -> gl.aw.|.io.
gl.oywi. -> gl.oy.|.wi.
g.wayw.ff|.o.n - > g.wa.|.yw.ff|.o.n

"""

# import re
# import unidecode

from bardd.base import TreeNode
from bardd.cyfres import Cyfres

from bardd.cysonion import (
    # llafariaid,
    # llafariaid_ysgafn,
    # llafariaid_trwm,
    # cytseiniaid,
    # atalnodau,
    deuseiniaid,
    dosbarth_deusain,
    # cyfuniadau_trychben,
    # eithriadau,
)

import logging
log = logging.getLogger(__name__)


class Sillaf(TreeNode):
    """
    Rhestr trefnedig o dri gwrthrych `Cyfres`:
        [cyrch, cnewyllyn, coda]
    """

    def __init__(self, cyrch="", cnewyllyn="", coda="", parent=None):
        TreeNode.__init__(self, parent=parent)

        self.children.append(Cyfres(cyrch))
        self.children.append(Cyfres(cnewyllyn))
        self.children.append(Cyfres(coda))

    def __str__(self):
        return "".join([str(cyfres) for cyfres in self.children])

    def __repr__(self):
        return ".".join([str(cyfres) for cyfres in self.children])

    def sain(self):
        return "".join([cyfres.sain() for cyfres in self.children])

    def cyrch(self):
        return self.children[0]

    def cnewyllyn(self):
        return self.children[1]

    def coda(self):
        return self.children[2]

    def odl(self):
        return (self.cnewyllyn(), self.coda())

    def nodau(self):
        return [nod for cyfres in self.children for nod in cyfres.children]

    # def rhestr_llafariaid(self):
    #     return [nod for nod in self.nodau() if nod.is_llafariad()]

    def nifer_llafariaid(self):
        return len(self.llafariaid())

    def is_llafarog(self):
        return not len(self.coda()) > 0

    # def rhestr_cytseiniaid(self, reverse=False):
    #     c = [nod for nod in self.nodau() if nod.is_cytsain()]
    #     if reverse:
    #         c.reverse()
    #     return c

    def prif_lafariad(self):

        # dileu atalnodau e.e. a'i, o'u, ayb)
        nodau = self.cnewyllyn().llafariaid()
        # [nod for nod in self.children[1].children if nod.is_llafariad()]

        # cnewyll unsain
        if len(nodau) == 1:
            return nodau[0]

        # cnewyll deusain
        #   lleddf: acen ar y llarariad cyntaf
        #       falling diphthong: 'aw', 'ew', 'ai', 'eu', ...
        #   talgron: acen ar yr ail lafariad
        #       rising diphthong: 'ia', 'ie', 'we', 'wi', ...
        elif len(nodau) == 2:
            ds = nodau[0].byr().text.lower() + nodau[1].byr().text.lower()
            if ds in dosbarth_deusain:
                if ds in deuseiniaid["lleddf"]:
                    return nodau[0]
                else:
                    return nodau[1]

        # trisain (acen bob amser ar y llafariad canol)
        elif len(nodau) == 3:
            return nodau[1]

        # caiff clymau pedwarsain eu hollti pan yn creu
        # sillafau felly dyle ni ddim cyrraedd fan hyn ...
        return None


# ------------------------------------------------
def main():
    test_data = (
        # unigol
        ('c', 'a', 'r'),
        ('c', 'i', 'st'),
        # ds
        ('', 'ia', 'dd'),
        ('', 'ae', 'l'),
        ('', 'yw', ''),
        # ('', '', ''),
    )

    for triawd in test_data:
        cy = triawd[0]
        cn = triawd[1]
        co = triawd[2]
        sill = Sillaf(cy, cn, co)
        print("-------------------")
        print(sill)
        pv = sill.prif_lafariad()
        print('prif lafariad: ', pv)
    print("-------------------")


if __name__ == "__main__":
    main()
