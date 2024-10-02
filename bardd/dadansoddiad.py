# dadansoddiad.py

from bardd.llinell import Llinell
from bardd.cwpled import Cwpled
from bardd.pennill import Pennill

from bardd.cysonion import colormaps, llythrenwau
from bardd.beiro import Beiro

# from profwr_llinellau import prawf_llinell
# from profwr_cwpledi import prawf_cwpled

# from bardd.lliwiau import Beiro


class Dadansoddiad():

    def __init__(self, uned=None):
        if uned and not type(uned) in (Llinell, Cwpled, Pennill):
            raise ValueError('Mae angen `Llinell`, `Cwpled` neu `Pennill` fan hyn.')

        self.uned = uned
        self.dosbarth = None
        self.gwallau = []       # rhestr llinynau
        self.hysbys = []        # rhestr llinynau 
        self.nodau = {}         # `list` (odl) neu `dict` (cyts)
        self.beiro = Beiro()

    def __str__(self):
        return self.adroddiad()

    def adroddiad(self):

        # init
        s = []

        s.append('---------------')
        
        if type(self.uned) is Llinell:
            if self.dosbarth:
                dosb = llythrenwau['cynghanedd'][self.dosbarth]
            else:
                dosb = llythrenwau['cynghanedd']['DIM']
            s.append(dosb)
            
            s.append('Nifer sillafau: ' + str(self.uned.nifer_sillafau()))
            # if str(self.uned.sain()) != str(self.uned):
            #     s.append('Seineg: ' + str(self.uned.sain()))
            
            if self.gwallau:
                print('Gwallau: ', self.gwallau)
        
        elif type(self.uned) is Cwpled:
            pass
        
        elif type(self.uned) is Pennill:
            pass

        else:
            pass


        # pob dosbarth ...
        if self.gwallau:
            s.append('\n'.join(self.gwallau))

        if self.hysbys:
            s.append('\n'.join(self.hysbys))

        if self.nodau:
            if type(self.nodau) is list:
                s.append(str(self.nodau))

            elif type(self.nodau) is dict:
                for key in self.nodau:
                    s.append('{}: {}'.format(key, self.nodau[key]))

        if hasattr(self, 'odl') and type(self.odl) is Dadansoddiad:
            s.append('Odl: ' + str(self.odl.nodau))

        if hasattr(self, 'cytseinedd') and type(self.cytseinedd) is Dadansoddiad:
            # print('DOSB_CYTS: ', self.cytseinedd.dosbarth)
 
            if self.cytseinedd.dosbarth not in [None, 'LLA', 'GWA']:
                if self.cytseinedd.nodau and type(self.cytseinedd.nodau) is dict:
                    s.append('Cytseinedd: ')
                    for key in self.cytseinedd.nodau:
                        s.append(' {}: {}'.format(key, self.cytseinedd.nodau[key]))

            if self.cytseinedd.dosbarth in ['GWA']:
                s.append('Gwallau: ' + str(self.cytseinedd.gwallau))

        return '\n'.join(s)

    def fancy(self, verbose=False, cmap=colormaps['disglair']):

        #
        # Fan hyn mae angen datod y seinegoli
        # drwy'r ddefnyddio'r rhestr trosiadau
        # if nod in self.trosiadau:
        #   ailosod y nodau gwreiddiol cyn dangos
        #
        # Mae angen ddefnyddio `dict` am y trosiadau
        # wedi ei fynegeio gan y nodau newydd.

        # type check
        if type(self.uned) is Llinell:
            return self.dangos_llinell(cmap=cmap)

        elif type(self.uned) is Cwpled:
            return self.dangos_cwpled(cmap=cmap)

        elif type(self.uned) is Pennill:
            return self.dangos_pennill(cmap=cmap)

        else:
            raise ValueError('Mae angen `Llinell`, `Cwpled` neu `Pennill` fan hyn.')

    def dangos_llinell(self, cmap=None):

        s = []
        s.append(self.uned.llinyn_acenion())

        od = self.dangos_odl(cmap=cmap)
        if od:
            s.append(od)
        else:
            s.append(str(self.uned))

        # os oes dosbarthiad (cywir neu wallus)
        if self.dosbarth:

            # dangos llinell cytseinedd
            cyts = self.dangos_cytseinedd(cmap=cmap)  # llinyn cytseiniaid
            if cyts:
                s.append(cyts)

            # lookup
            dosb = llythrenwau["cynghanedd"][self.dosbarth]

            # gwallus
            if self.dosbarth in ['GWA',]:
                s.append(self.beiro.coch(dosb))
                # s.append('xxx')
                # s.append(str(self.gwallau))
                s.append(self.beiro.amryliw('\n'.join(self.gwallau), lliw=cmap['toriad']))

            # pengoll
            elif self.dosbarth in ['CBG', 'TBG']:
                s.append(self.beiro.melyn(dosb))

            # llwyddiant
            else:
                s.append(self.beiro.cyan(dosb))

        # dim modd dosbarthu
        else:
            # print('DIM BYD')
            # s.append(self.uned.llinyn())
            dosb = llythrenwau["cynghanedd"]['DIM']
            s.append(self.beiro.coch(dosb))
            # s.append(self.adroddiad())
            # s.append('xxx')

        # print(s)
        return '\n'.join(s)

    def dangos_cwpled(self, cmap=colormaps['disglair']):
 
        s = []
        if self.dosbarth:
            s.append(self.uned.cyntaf.show())
            s.append(self.uned.ail.show())
            s.append(self.beiro.gwyrdd(self.dosbarth))
        else:
            s.append(self.uned.llinyn())
            s.append(self.beiro.coch('XXX'))
        return '\n'.join(s)

    def dangos_pennill(self, cmap=None):
        s = []
        sep = '---------------'
        if self.dosbarth:

            if hasattr(self, 'llinellau'):
                for dad in self.llinellau:
                    s.append(self.dad.show())
                    s.append(self.beiro.gwyrdd(dad.dosbarth))
                else:
                    s.append(dad.uned.llinyn())
                    s.append(self.beiro.coch('XXX'))

            if hasattr(self, 'cwpledi'):
                for dad in self.cwpledi:
                    s.append(self.dad.show())
                    s.append(self.beiro.gwyrdd(dad.dosbarth))
                else:
                    s.append(dad.uned.llinyn())
                    s.append(self.beiro.coch('XXX'))
        else:
            s.append(self.uned.llinyn())
            s.append(self.beiro.coch('XXX'))

            s.append(sep)
        return '\n'.join(s)

    def dangos_odl(self, blanksymbol=' ', popeth=True, cmap='disglair'):

        # check
        # if not self.dosbarth or not hasattr(self, 'odl'):
        if not hasattr(self, 'odl'):
            return None  # 'dim odl'
        
        if not hasattr(self.odl, 'nodau'):
            return None  # 'dim nodau odl'

        # if not self.odl.nodau:
        #     return None  # 'dim nodau odl'

        # print('odl.dosbarth = ', self.odl.dosbarth)
        # print('odl.nodau = ', self.odl.nodau)
        nodau_soniarus = [nod for cyfres in self.odl.nodau for nod in cyfres]
        # print('soniarus = ', nodau_soniarus)
        s = []
        for gair in self.uned.children:
            ss = []
            # print('nodau: ', gair.nodau())
            for nod in gair.nodau():
                if nod in nodau_soniarus:
                    # print('helo: ', nod)
                    ss.append(self.beiro.amryliw(nod.text, lliw=cmap['odl']))
                else:
                    if popeth:
                        ss.append(nod.text)
                    else:
                        ss.append(blanksymbol * len(nod.text))
                    # ss.append(nod.text.upper() * len(nod.text))
            s.append(''.join(ss))
        return blanksymbol.join(s)

    def dangos_cytseinedd(self, blanksymbol=' ', cmap='disglair'):
        '''
        Awk fan hyn: mae angen mynd fesul nod er mwyn
        mewnosod safleoedd y prif lafariaid fel colon,
         ond hefyd fesul gair er mwyn mewnosod safleoedd
         y gorffwysfeydd
        '''

        # type check
        if type(self.uned) is not Llinell:
            return None  # 'DIM LLINELL'
        if not self.dosbarth or not hasattr(self, 'cytseinedd'):
            return None  # 'DIM CYTSEINEDD'
        if not hasattr(self.cytseinedd, 'nodau'):
            return None  # 'DIM NODAU CYTSEINEDD'
 
        # dosbarthiadau nodau cytsain mewn trefn (er mwyn lliwio yn y drefn gywir)
        dosbyrth_didoledig = [
            'cyswllt',
            'cyfateb',
            'traws',
            'pengoll',
            'trychben',
            'cysylltben',
        ]

        # dolennu dros y geiriau
        s = []
        for gair in self.uned.children:

            # print(gair)

            # dolennu dros y nodau
            ss = []
            for nod in gair.nodau():

                # cnewyll colon
                if gair in self.gorffwysfeydd:
                    if self.dosbarth == 'SAI':
                        if gair == self.gorffwysfeydd[-1]:
                            if nod in gair.prif_lafariaid():
                                ss.append(':')
                                continue
                    elif self.dosbarth == 'SGA':
                        if gair == self.gorffwysfeydd[-2]:
                            if nod in gair.prif_lafariaid():
                                ss.append(':')
                                continue
                    else:
                        # if gair in self.gorffwysfeydd[-1]:
                        if nod in gair.prif_lafariaid()[-2:]:
                            ss.append(':')
                            continue

                if gair == self.uned.children[-1]:
                    if nod in gair.prif_lafariaid()[-2:]:
                        ss.append(':')
                        continue

                # chwilio trwy'r dosbyrth cytseiniaid
                darganfuwyd = False
                for dosb in dosbyrth_didoledig:

                    # if dosb == 'pengoll':
                    #     print('Hwre: ', dosb)
                    # print(self.cytseinedd.nodau)

                    # hepgor dosbyrth amherthnasol
                    if dosb not in self.cytseinedd.nodau:
                        continue

                    # fflatio rhestrau nythedig
                    elif dosb == 'cyfateb':  # angen fflatio parau
                        nodau_dethol = [x for par in self.cytseinedd.nodau[dosb] for x in par]

                    # popeth arall
                    else:
                        nodau_dethol = self.cytseinedd.nodau[dosb]

                    if nod in nodau_dethol:
                        # print('HELO: ', nod)
                        # print(gair.prif_lafariaid())
                        # print(key, cmap)
                        if cmap and dosb in cmap:
                            ss.append(self.beiro.amryliw(nod.text, lliw=cmap[dosb]))
                        else:
                            ss.append(nod.text)
                        darganfuwyd = True
                        break

                    # end iteru dros y dosbyrth

                # naddo
                if not darganfuwyd:
                    ss.append(blanksymbol * len(nod.text))

            # profi am safle toriad
            if gair in self.gorffwysfeydd:
                # print('>>', str(gair), '<<')
                if cmap and 'toriad' in cmap:
                    ss.append(self.beiro.amryliw('|', lliw=cmap['toriad']))
                else:
                    ss.append('|')
            else:
                # atodi bwlch
                if gair != self.uned.children[-1]:
                    # ss.append('+')
                    ss.append(blanksymbol)

            # atodi
            s.append(''.join(ss))

        return ''.join(s)

    def dangos_gorffwysfeydd(self, blanksymbol=' ', cmap=None):

        if not hasattr(self, 'gorffwysfeydd'):
            return blanksymbol * len(self.nodau())

        beiro = Beiro()
        s = []
        for gair in self.uned.children:
            s.append(blanksymbol * len(str(gair)))
            if gair in self.gorffwysfeydd:
                if cmap and 'gorffwysfeydd' in cmap:
                    s.append(beiro.amryliw('|', lliw=cmap['gorffwysfeydd']))
                else:
                    s.append('|')
            else:
                s.append(blanksymbol)

        return ''.join(s[:-1])

    def dangos_cnewyll_colon(self, char=':', blanksymbol=' ', cmap=None):

        s = []
        for gair in self.uned.children:

            # cyrchu prif lafariad pob cnewyllyn
            acenion = []
            if gair == self.uned.children[-1]:
                acenion = gair.acenion()
            if hasattr(self, 'gorffwysfeydd') and gair in self.gorffwysfeydd:
                acenion = gair.acenion()

            # dolennu dros y nodau
            ss = []
            for nod in gair.nodau():
                if nod in acenion:
                    ss.append(char)
                else:
                    ss.append(blanksymbol * len(nod.text))

            s.append(''.join(ss))

        return blanksymbol.join(s)


def main():
    pass


if __name__ == "__main__":
    main()
