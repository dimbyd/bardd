# allbwn.py
'''
Duliau er mwyn printio dadansoddiadau i'r console

input: dadansoddiad
output: str
'''

from bardd.cysonion import colormaps
from bardd.beiro import magenta, cyan, coch, gwyrdd, brwsh


def show_llinyn_odl(dad, blank=' '):

    if 'llinell' not in dad:
        return None

    if 'nodau_odl' not in dad:
        return str(dad['llinell'])

    geiriau = dad['llinell'].children
    a = []
    for gair in geiriau:
        b = []
        for nod in gair.nodau():
            if nod in dad['nodau_odl']:
                b.append(brwsh(nod.text, lliw=colormaps['odl']))
            else:
                b.append(nod.text)
        a.append(''.join(b))
    return ' '.join(a)


def show_llinyn_cytseinedd(dad, markup='plain', blank=' '):

    # type check
    if 'llinell' not in dad:
        return None

    # dosbarthiadau mewn trefn (er mwyn lliwio)
    nodau_cytseinedd = ['parau', 'traws', 'gwreiddgoll', 'trychben', 'cysylltben', 'cyswllt']

    # allbwn
    a = []

    # dolennu dros y geiriau
    geiriau = dad['llinell'].children
    for gair in geiriau:

        # cofnodi lleoliad acenion yr orffwysfa neu'r brifodl
        acenion = []
        if gair == geiriau[-1] or ('gorffwysfa' in dad and gair in dad['gorffwysfa']):
            acenion = gair.acenion()

        b = []
        # dolennu dros y nodau
        for nod in gair.nodau():

            # nodi lleoliad yr acenion
            if nod in acenion:
                b.append(':')
            else:
                # chwilo am y nod yn y rhestri nodau dethol
                found = False
                for key in nodau_cytseinedd:
                    if key not in dad['nodau_dethol']:
                        continue
                    elif key == 'parau':
                        nodau = [nod2 for par in dad['nodau_dethol'][key] for nod2 in par]
                    else:
                        nodau = dad['nodau_dethol'][key]

                    if nod in nodau:
                        if markup == 'bash':
                            b.append(brwsh(nod.text, lliw=colormaps[key]))
                        else:
                            b.append(nod.text)
                        found = True
                        break

                # replace others by blanks
                if not found:
                    b.append(blank * len(nod.text))

        a.append(''.join(b))

        # nodi toriadau
        if 'gorffwysfa' in dad and gair in dad['gorffwysfa']:
            a.append('|')
        else:
            a.append(blank)

    return ''.join(a)


def show_dadansoddiad(dad, verbose=False):

    # type check
    if not (type(dad) is dict):
        raise ValueError('Mae angen `dict` fan hyn.')

    if 'llinell' in dad.keys():
        show_dadansoddiad_llinell(dad, verbose=verbose)
    elif 'cwpled' in dad.keys():
        show_dadansoddiad_cwpled(dad, verbose=verbose)
    elif 'pennill' in dad.keys():
        show_dadansoddiad_pennill(dad, verbose=verbose)
    else:
        raise ValueError('Mae angen `Llinell`, `Cwpled` neu `Pennill` fan hyn.')


def show_dadansoddiad_llinell(dad, verbose=False):

    # type check
    if not (type(dad) is dict):
        raise ValueError('Mae angen `dict`  fan hyn.')
    if 'llinell' not in dad.keys():
        raise ValueError('Mae angen dadansoddiad llinell fan hyn.')

    ll = dad['llinell']
    s = []
    s.append(ll.llinyn_acenion())
    if dad['dosbarth']:
        s.append(show_llinyn_odl(dad))
        s.append(show_llinyn_cytseinedd(dad, markup='bash'))
        s.append(magenta(dad['dosbarth']))
    else:
        s.append(ll.llinyn())
        s.append(coch('XXX'))

    if verbose:
        for key in ['dosbarth', 'gorffwysfa', 'nodau_dethol']:
            if key in dad and dad[key]:
                s.append('{} : {}'.format(key, str(dad[key])))

    return '\n'.join(s)


def show_dadansoddiad_cwpled(dad, verbose=False):

    if (type(dad) is not dict):
        raise ValueError('Mae angen `dict` fan hyn.')
    if 'cwpled' not in dad.keys():
        raise ValueError('Mae angen dadansoddiad cwpled fan hyn.')

    # copio'r odlau i restri nodau dethol y llinellau unigol
    # fel hyn byddant yn cael eu lliwio gyda nodau soniarus
    # erall sy'n perthyn i'r llinell yn unigol (h.y. lusg neu sain)
    if 'nodau_soniarus' in dad:
        if 'dad_cyntaf' in dad:
            if 'nodau_dethol' in dad['dad_cyntaf']:
                if 'soniarus' in dad['dad_cyntaf']['nodau_dethol']:
                    dad['dad_cyntaf']['nodau_dethol']['soniarus'].extend(dad['nodau_soniarus'])
                else:
                    dad['dad_cyntaf']['nodau_dethol']['soniarus'] = dad['nodau_soniarus']
        if 'dad_ail' in dad:
            if 'nodau_dethol' in dad['dad_ail']:
                if 'soniarus' in dad['dad_ail']['nodau_dethol']:
                    dad['dad_ail']['nodau_dethol']['soniarus'].extend(dad['nodau_soniarus'])
                else:
                    dad['dad_ail']['nodau_dethol']['soniarus'] = dad['nodau_soniarus']

    s = []
    sep = '--------------------'
    s.append(show_dadansoddiad_llinell(dad['dad_cyntaf'], verbose=verbose))
    s.append(sep)
    s.append(show_dadansoddiad_llinell(dad['dad_ail'], verbose=verbose))
    s.append(sep)
    if dad['dosbarth']:
        s.append(cyan(dad['dosbarth']))
    else:
        s.append(coch('XXX'))
    if verbose:
        for key in ['dosbarth', 'nodau_soniarus', 'dad_cyntaf', 'dad_ail']:
            if key in dad and dad[key]:
                print('{} : {}'.format(key, str(dad[key])))
    s.append(sep)
    return '\n'.join(s)


def show_dadansoddiad_pennill(dad, verbose=False):

    # type check
    if type(dad) is not dict:
        raise ValueError('Mae angen `dict` fan hyn.')
    if 'pennill' not in dad.keys():
        raise ValueError('Mae angen pennill fan hyn.')

    s = []
    sep = '------------------------------'
    if 'dads' in dad:
        for dad_isran in dad['dads']:
            if 'cwpled' in dad_isran:
                s.append(show_dadansoddiad_cwpled(dad_isran, verbose=verbose))
            elif 'llinell' in dad_isran:
                s.append(show_dadansoddiad_llinell(dad_isran, verbose=verbose))

    if dad['dosbarth']:
        print(gwyrdd(dad['dosbarth']))
    else:
        print(coch('XXX'))

    s.append(sep)
    return '\n'.join(s)
