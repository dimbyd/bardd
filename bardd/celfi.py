# celfi.py
'''
1. odliadur (regex)
2. cleciadur (regex)
3. chwiliadur (regex)
4. treilliwr (prawf_llinell)

'''
import re
from bardd.settings import DATABASES
from bardd.cysonion import llafariaid, cytseiniaid
from bardd.cysonion import eithriadau
from bardd.gair import Gair

odlau_file = DATABASES['default']['ODLAU']    # json
geirfa_file = DATABASES['default']['GEIRFA']  # txt

lluosill_acennog = eithriadau['lluosill_acennog']
deusain_ddeusill = eithriadau['deusain_ddeusill']


def rhestr_nodau(s):
    nodau = []
    chars = list(s)
    idx = 0
    while idx < len(chars):
        if idx < len(chars) - 1 and ''.join([chars[idx], chars[idx + 1]]) in cytseiniaid:
            nodau.append(''.join([chars[idx], chars[idx + 1]]))
            idx += 1
        else:
            nodau.append(chars[idx])
        idx += 1
    return nodau


def rhestr_clymau(s):

    nodau = rhestr_nodau(s)
    clymau = []
    idx = 0
    cwlwm = []

    if nodau and nodau[0] not in cytseiniaid:
        clymau.append([])

    while idx < len(nodau):
        if (
            len(cwlwm) == 0 or 
            (nodau[idx] in llafariaid and cwlwm[0] in llafariaid) or            
            (nodau[idx] in cytseiniaid and cwlwm[0] in cytseiniaid)
        ):
            cwlwm.append(nodau[idx])
        else:
            clymau.append(cwlwm)
            cwlwm = [nodau[idx]]
        idx += 1

    clymau.append(cwlwm)
    if clymau and clymau[-1][0] not in cytseiniaid:
        clymau.append([])

    return clymau


def nifer_sillafau(s):
    return int(len(rhestr_clymau(s)) / 2)


def lluosill(s):
    return nifer_sillafau(s) > 1


def acennog(s):
    # if nifer_sillafau(s) == 1 or s in geiriau_lluosill_acennog:
    if Gair(s).acennog() or s in lluosill_acennog:
        return True
    return False


def traeannu(s):
    clymau = rhestr_clymau(s)
    if lluosill(s) and not acennog(s):
        return (clymau[:-4], clymau[-4:-2], clymau[-2:])
    else:
        return (clymau[:-2], clymau[-2:], [])


def cytbwys(s1, s2):
    if (acennog(s1) and acennog(s2)) or (not acennog(s1) and not acennog(s2)):
        return True
    return False


def creu_patrwm_clec(s, cytbwys=True):
    '''
    Creu myngegiad rheolaidd
    '''

    llaf = '|'.join(llafariaid)
    cyts = '|'.join(cytseiniaid)

    b, c, d = traeannu(s)

    vb = b[1::2] if b else []  # clymau llafariaid y blaen
    cb = b[::2] if b else []   # clymau cytseiniaid y blaen

    # fflatio
    vb = [x for cwlwm in vb for x in cwlwm]
    cb = [x for cwlwm in cb for x in cwlwm]

    # convert to str
    # cbs = ''.join(cb)
    # vbs = ''.join(vb)
    vcs = ''.join(c[0])
    ccs = ''.join(c[1])
    vds = ''.join(d[0]) if (d and d[0]) else []
    cds = ''.join(d[1]) if (d and d[1]) else []

    # init
    p = []
    
    # cytseiniaid blaen
    # p.append(r'[' + llaf2 + ']*')
    for idx, c in enumerate(cb):
        p.append('({}|{})'.format(c.lower(), c.title()))
        if idx < len(cb) - 1:
            p.append(r'[' + llaf + ']*')

    # cytbwys
    if cytbwys:

        # cytbwys acennog
        if acennog(s):

            # llafariad dan yr acen yn wahanol
            if vcs:
                p.append(r'(?!' + vcs + r')')
            p.append('[' + llaf + r']+')

            # cytseiniaid dan yr acen yn wahanol
            if ccs:
                p.append(r'(?!' + ccs + r')')
            p.append(r'[' + cyts + ']*')

        # cytbwys ddiacen
        else:

            # llafariad dan yr acen yn wahanol
            if vcs:
                p.append(r'(?!' + vcs + r')')
            p.append('[' + llaf + r']+')

            # cytseiniaid dan yr acen yn cysefeillio
            if ccs:
                p.append(ccs + r'(?![' + cyts + '])')

            # llafariad y sill olaf yn wahanol (oes angen hwn?)
            if vds:
                # p.append(r'(?!' + vds + r')')
                pass
            p.append('[' + llaf + r']*')

            # cytseiniaid y sill olaf yn wahanol
            if cds:
                p.append(r'(?!' + cds + r')')
            p.append(r'[' + cyts + ']*')

    # angytbwys
    else:

        # anghytbwys ddiacen (ddisgynedig)
        if acennog(s):

            # llafariaid dan yr acen yn wahanol
            if vcs:
                p.append(r'(?!' + vcs + r')')
            p.append('[' + llaf + r']+')

            # cytseiniaid dan yr acen yn cysefeillio
            if ccs:
                p.append(ccs + r'[' + llaf + ']+')
            p.append('[' + cyts + r']*')

        # anghytbwys acennog (ddyrchafedig)
        else:

            # llafariaiad dan yr acen yn wahanol
            if vcs:
                p.append(r'(?!' + vcs + r')')
                p.append('[' + llaf + r']+')

            # cytseiniaid dan yr acen yn cysefeillio
            if ccs:
                p.append(ccs + r'[' + llaf + ']*')
                # p.append(ccs + r'(?![' + cyts + '])')

    return r''.join(p)


def clec(p, s):
    if re.fullmatch(p, s):
        return True
    return False


def cleciadur(s):
    '''
    Cleciadur: darganfod geiriau sy'n cynganeddu gyda'r gofyniad.
    '''
    # geirfa
    with open(geirfa_file, encoding='utf-8-sig') as f:
        s0 = f.read()
        geirfa = s0.strip().split('\n')
        # geirfa = [Gair(s2) for s2 in s1]

    # info
    # print('Geirfa:   {}'.format(len(geirfa)))
    # print('Gofyniad: {}'.format(s))

    # creu patrymau rhelaidd
    p_cytbwys = creu_patrwm_clec(s, cytbwys=True)
    p_anghytbwys = creu_patrwm_clec(s, cytbwys=False)

    # info
    # print(p_cytbwys)
    # print(p_anghytbwys)

    clecs = []
    for s2 in geirfa:
        if cytbwys(s, s2) and clec(p_cytbwys, s2):
            clecs.append(s2)
        if not cytbwys(s, s2) and clec(p_anghytbwys, s2):
            clecs.append(s2)

    return clecs


def odliadur(s, odl_lusg=False, acennog_yn_unig=False):

    # defnyddio odliadur RS am odlau syml
    if not odl_lusg:
        import json
        with open(odlau_file, "r") as infile:
            odliadur = json.load(infile)
        if s in odliadur:
            odlau = odliadur[s]
            if acennog_yn_unig:
                odlau = [od for od in odlau if acennog(od)]
            return odlau if odlau else None

    # defnyddio geiriau JGJ am odlau llusg
    import re
    with open(geirfa_file) as f:
        s0 = f.read()
    llaf = '|'.join(llafariaid)
    cyts = '|'.join(cytseiniaid)
    if odl_lusg:
        p = r'\b[a-z]*' + r'[' + cyts + r']+' + s + r'[' + llaf + r']+[' + cyts + ']*' + r'\b'
    else:
        p = r'\b[a-z]*' + s + r'\b'

    odlau = re.findall(p, s0)
    return odlau if odlau else None


def main():
    s = 'cariad'
    # s = 'nant'
    # s = 'ffenest'
    # s = 'afon'
    # s = 'corrach'

    print('YMHOLIAD: {}'.format(s))

    clecs = cleciadur(s)
    if clecs:
        print('CLECS:\n' + ' '.join(clecs))

    s = 'afiach'

    odlau = odliadur(s)
    if odlau:
        print('ODLAU:\n' + '  '.join(odlau))

    odlau = odliadur(s, acennog_yn_unig=True)
    if odlau:
        print('ODLAU ACENNOG:\n' + ' '.join(odlau))

    odlau = odliadur(s, odl_lusg=True)
    if odlau:
        print('ODLAU LLUSG:\n' + ' '.join(odlau))


if __name__ == '__main__':
    main()
