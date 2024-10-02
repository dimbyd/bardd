# acen.py
'''
Dulliau ar gyfer darganfod dosbarth aceniad.

mewnbwn: dau wrthrych `Gair` (yr orffwysfa a'r brifodl)

allbwn: llythrenw dosbarth aceniad
	'CAC': cytbwys acennog
	'CDI': cytbwys ddiacen
	'ADI': angytbwys ddisgynedig
	'ADY': angytbwys ddyrchafedig
'''

from bardd.gair import Gair

def aceniad(g1, g2):
    '''
    ffwythiant:	darganfod dosbarth aceniad dau air
    mewnbwn:	dau air (yr orffwysfa a'r brifodl)
    allbwn:		llythrenw dosbarth aceniad (CAC,CDI,ADI,ADY)
    '''
    if g1.is_acennog():
        if g2.is_acennog():
            return 'CAC'
        else:
            return 'ADI'
    else:
        if g2.is_acennog():
            return 'ADY'
        else:
            return 'CDI'
