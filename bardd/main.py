# main.py

import os
import re
import sys

from optparse import OptionParser
import logging

from bardd.cysonion import geiriau_gwan

from bardd.gair import Gair
from bardd.llinell import Llinell
from bardd.cwpled import Cwpled
from bardd.pennill import Pennill

from bardd.seineg import seinegoli_fesul_sillaf

from bardd.dilyswr_llinellau import prawf_llinell
from bardd.dilyswr_cwpledi import prawf_cwpled
from bardd.dilyswr_penillion import prawf_pennill

from bardd.beiro import Beiro

from bardd.settings import LOG_FILE_NAME
from bardd.settings import DATABASES
odlau_file = DATABASES['default']['ODLAU']        # json
geirfa_file = DATABASES['default']['GEIRFA']      # txt


class Efrydydd(object):
    '''
    Mae angen opts ar gyfer:
    meddalu, caledu, odlau deheuol ayb
    '''

    def __init__(self, infile=None):
        self.unedau = []
        if infile:
            self.unedau = self.darllen(infile)
        self.seinegol = False
        self.caledu = False
        self.beiro = Beiro()

        logging.info('Efrydydd newydd.')

    def __str__(self):
        return r'\n\n'.join([str(uned) for uned in self.unedau])

    def __repr__(self):
        return r'\n\n'.join([repr(uned) for uned in self.unedau])

    def darllen(self, infile):
        '''
        Darllen llinellau, cwpledi a phenillion
            - llinell wag rhwng penillion
            - dwy linell wag rhwng cerddi
        '''
        with open(infile) as f:

            str0 = f.read()
            str_cerdd = str0.strip().split(r'\n\n')
            unedau = []

            for str_pennill in str_cerdd:
                str_llinellau = str_pennill.strip().split('\n')
                llinellau = []

                for s in str_llinellau:

                    # anwybyddu sylwadau
                    if re.search(r'^#', s) or re.search(r'^\s*$', s):
                        continue

                    # creu gwrthrych Llinell
                    llinell = Llinell(s)
                    seinegoli_fesul_sillaf(llinell, meddalu=True, caledu=True)
                    llinellau.append(llinell)

                # storio llinell unigol fel `Llinell`
                if len(llinellau) == 1:
                    unedau.append(llinellau[0])

                # fel arall, storio fel `Pennill`
                else:
                    unedau.append(Pennill(llinellau))

        return unedau

    def dadansoddwr(self, uned):

        if type(uned) is Llinell:
            return prawf_llinell(uned, seinegol=self.seinegol)

        elif type(uned) is Cwpled:
            return prawf_cwpled(uned, seinegol=self.seinegol)

        elif type(uned) is Pennill:
            return prawf_pennill(uned, seinegol=self.seinegol)

        else:
            msg = 'Mae angen `Llinell`, `Cwpled` neu `Pennill` fan hyn.'
            raise TypeError(msg)
        
    def treilliwr(self, s):
        '''
        Darganfod cynghanedd mewn rhyddiaith
        input:  str
        return: rhestr o ddadansodiadau
        '''
        # params
        # nifer_sillafau_lleiaf = 6
        # nifer_sillafau_mwyaf = 10
        nifer_sillafau_lleiaf = 7
        nifer_sillafau_mwyaf = 7

        # echdynnu brawddegau
        brawddegau = s.split('.')
        brawddegau = [br.strip() + '.' for br in brawddegau]

        # creu rhestr dadansoddiadau
        dads = []

        # dolennu dros y brawddegau
        for braw in brawddegau:

            # gwirio am sylwadau
            if not braw or braw[0] == '#':
                continue

            # echdynnu rhestr geiriau
            # ss = [s.strip() for s in braw.split(' ')]
            ss = [s.strip() for s in braw.split()]
            geiriau = [Gair(s) for s in ss]

            idx_chw = 0
            idx_dde = 1

            # creu llinellau
            while idx_dde < len(geiriau):

                while idx_dde < len(geiriau) and sum([g.nifer_sillafau() for g in geiriau[idx_chw: idx_dde]]) < nifer_sillafau_lleiaf:
                    idx_dde = idx_dde + 1

                while sum([g.nifer_sillafau() for g in geiriau[idx_chw:idx_dde]]) > nifer_sillafau_mwyaf:
                    idx_chw = idx_chw + 1

                # profi am air gwan yn y brifodl:
                if str(geiriau[idx_dde - 1]).lower() not in geiriau_gwan:

                    llinell = Llinell(geiriau[idx_chw:idx_dde])
                    dads2 = prawf_llinell(llinell, min_sillafau=2, max_sillafau=10)

                    # hidlo
                    dim_diolch = ['GWA', 'TRF', 'LLL', 'SAL', 'CBG', 'TBG']
                    for dad in dads2:
                        if dad.dosbarth and dad.dosbarth not in dim_diolch:
                            dads.append(dad)

                    # # hidlo cynghanedd pengoll (CBG, TBG)
                    # dads2 = [dad for dad in dads2 if dad.dosbarth not in ['CBG', 'TBG']]

                    # # hidlo TRF, LLL, SAL
                    # for dad in dads2:
                    #     if dad.dosbarth and dad.dosbarth not in ['TRF', 'LLL', 'SAL']:
                    #         dads.append(dad)

                # symud i'r gair nesaf
                # idx_chw = idx_chw + 1
                idx_dde = idx_dde + 1

        return dads

    def odliadur(self, qstr, odl_lusg=False, acennog_yn_unig=False):
        from bardd.celfi import odliadur
        return odliadur(qstr,
                        odl_lusg=odl_lusg,
                        acennog_yn_unig=acennog_yn_unig)

    def cleciadur(self, qstr):
        from bardd.celfi import cleciadur
        return cleciadur(qstr)


# demos (ddim yn rhan o'r gwrthrych Efryd)
def demo_penillion():
    '''
    Mae hwn yn fregus
    '''
    dir_name = 'cronfa/penillion/'
    input_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), dir_name)
    filenames = [
        'englynion/englyn_y_bardd_trwm.txt',
        'englynion/englyn_y_gorwel.txt',
        'cywyddau/cywydd_tudur_aled.txt',
        'cywyddau/cywydd_i_ofyn_march.txt',
        'cywyddau/cywydd_croeso_amgen_2020.txt',
        'cywyddau/cywydd_edifeirwch.txt',
        'cywyddau/morfudd_fel_yr_haul.txt',
        'eraill/hir_a_thoddaid_gwaddol.txt',
        'cywyddau/cywydd_clera.txt',
    ]

    ef = Efrydydd()
    for filename in filenames:
        infile = os.path.join(input_dir, filename)
        ef.read_unedau(infile)
        dads = [ef.dadansoddwr(uned) for uned in ef.undeau]

        for dad in dads:
            print(dad)
            print(dad.fancy())

    # allbwn
    print('===================')
    for uned in ef.unedau:
        print('-------------------')

        if type(uned) is Llinell:
            dad = prawf_llinell(uned)
            print(dad.fancy())

        elif type(uned) is Pennill:
            for llinell in uned.children:
                dad = prawf_pennill(uned)
                print(dad.fancy())

        else:
            print('Mae angen `Llinell` neu `Pennill` fan hyn.')
            continue


def demo(verbose=False):

    from subprocess import call
    from bardd.data_llinellau import profion

    from bardd.dadansoddiad import Dadansoddiad

    for dosbarth, test_cases in profion.items():
        call(["clear"])
        print('========================================')
        print(dosbarth.upper())
        print('========================================')
        for test_case in test_cases:
            llinell = Llinell(test_case)
            seinegoli_fesul_sillaf(llinell, meddalu=True, caledu=True)

            dads = prawf_llinell(llinell)
            # print([dad.dosbarth for dad in dads])
            
            if not dads:
                dad = Dadansoddiad(llinell)
            
            # elif len(dads) == 1 and dads[0].dosbarth in ['CBG','TBG']:
            #     dad[0]= Dadansoddiad(llinell)
            
            # hidlo CBG a TBG
            if len(dads) > 1:
                dads = [dad for dad in dads if dad.dosbarth not in ['CBG', 'TBG']]

            for dad in dads:
                print(dad.fancy())
                # if verbose:
                #     print(dad.adroddiad())

                if not dad == dads[-1]:
                    print('---')
            print('----------------------------------------')
        try:
            # input(">> bwrwch y dychwelwr i barhau ...")
            input("...")

        except KeyboardInterrupt:
            print(' Beth?')
            return


def main(args=None):
    '''
    Entry point.
    store_true means false by default (i.e. if unset)
    '''
    # dewisiadau
    parser = OptionParser(
                usage="%prog [-v] [-q] [-d] [-p] [-r] [llinyn] [-i infile]",
                version="%prog: fersiwn 0.1", add_help_option=False)
    parser.add_option("--debug",
                      dest="debug",
                      action="store_true",
                      help="debug mode")
    parser.add_option("-v", "--verbose", 
                      dest="verbose",
                      action="store_true",
                      help="verbose")
    parser.add_option("-q", "--quiet",
                      dest="quiet",
                      action="store_true",
                      help="cryno")
    parser.add_option("-p", "--profion",
                      dest="profion",
                      action="store_true",
                      help="demo/test")
    parser.add_option("-m", "--mewn",
                      dest="mewn",
                      help="ffeil utf-8")
    parser.add_option("-o", "--odl",
                      dest="odl",
                      help="odliadur")
    parser.add_option("-c", "--clec",
                      dest="clec",
                      help="cleciadur")
    parser.add_option("-g", "--gair",
                      dest="gair",
                      help="ymholiad chwiliadur")
    parser.add_option("-d", "--dadansoddwr",
                      dest="dadansoddwr",
                      action="store_false",
                      help="dadansoddiad llinellau/penillion (default)")
    parser.add_option("-t", "--treilliwr",
                      dest="treilliwr",
                      action="store_true",
                      help="chwilio am gynghanedd mewn rhyddiaith")
    parser.add_option("-l", "--lusg",
                      dest="lusg",
                      action="store_true",
                      help="chwilio am odlau llusg")
    parser.add_option("-a", "--acennog",
                      dest="acennog",
                      action="store_true",
                      help="chwilio am eiriau acennog yn unig")
    parser.add_option("-s", "--seinegol",
                      dest="seinegol",
                      action="store_true",
                      help="mewnbwn seinegol (IPA)")
    parser.add_option("-h", "--help",
                      action="help",
                      help="help")
    # parser.set_defaults(verbose=False, demo=False, testun=False)

    logging.debug('Helo from debug (main.py)!')

    # prosesu opsiynnau
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    input_str = ''
    if not args:
        args = sys.argv[1:]
    else:
        input_str = args[0]     # llinell unigol (utf-8)

    # init
    ef = Efrydydd()
    if options.seinegol:
        ef.seinegol = True

    # 1. llinell unigol
    if input_str:
        logging.info('Prawf llinell unigol.')
        dads = ef.dadansoddwr(Llinell(input_str))
        for dad in dads:
            print(dad.fancy(dad))
            if options.verbose:
                print(dad.adroddiad())

    # 1b. odliadur
    elif options.odl:
        qstr = options.odl
        logging.info('Odliadur: {}'.format(qstr))
        if options.lusg:
            odlau = ef.odliadur(qstr, odl_lusg=True)
        else:
            odlau = ef.odliadur(qstr, acennog_yn_unig=options.acennog)
        if odlau:
            print(ef.beiro.cyan(' '.join(odlau)))

    # 1c. cleciadur
    elif options.clec:
        qstr = options.clec
        logging.info('Cleciadur: {}'.format(qstr))
        clecs = ef.cleciadur(qstr)
        if clecs:
            print(ef.beiro.cyan(' '.join(clecs)))

    # 1d. chwiliadur
    elif options.gair:
        qstr = options.gair
        logging.info('Chwiliadur: {}'.format(qstr))
        return []

    # 2. demo
    elif options.profion:
        demo(verbose=options.verbose)

    # 3. rhyddiaith
    elif options.mewn and options.treilliwr:

        dads = []
        with open(options.mewn) as f:
            s = f.read()
            dads = ef.treilliwr(s)

        print('------------------------------')
        for dad in dads:
            print(dad.fancy())
            print('------------------------------')

    # 4. Dadansoddi llinellau/penillion
    # Mae angen \n rhwng bob llinell a \n\n rhwng bob pennill
    else:
        if options.mewn:
            with open(options.mewn) as f:
                lines = f.readlines()
        else:
            lines = sys.stdin.read().split('\n')

        # check
        if not lines:
            print('Beth?')
            return

        for s in lines:
            if re.search(r'^#', s) or re.search(r'^\s*$', s):
                continue
            llinell = Llinell(s.strip())
            seinegoli_fesul_sillaf(llinell)
            dads = ef.dadansoddwr(llinell)

            # hidlo cynghanedd traws bengoll
            dads = [dad for dad in dads if dad.dosbarth not in ['TBG']]

            print('----------------------------------------')
            if dads:
                for dad in dads:
                    print(dad.fancy())
                    if options.verbose:
                        print(dad.adroddiad())
            else:
                print(llinell)
                print(Beiro().coch('DIM'))

        print('----------------------------------------')


if __name__ == '__main__':

    import logging
    logging.basicConfig(
        filename=LOG_FILE_NAME,
        filemode='w',
        encoding='utf-8',
        level=logging.DEBUG,
    )
    logging.info('Dechrau')
    main()
    logging.info('Diwedd')
