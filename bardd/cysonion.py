# cysonion.py (constants)

"""
nodau:		llafariaid, cytseiniaid, atalnodau, deuseiniaid,
cytseinedd: cyfuniadau caled, cyfuniadau meddal, cyfuniadau trychben,
odl: 		cyfuniadau gwyrdro
dadansoddi:	llythrenwau
cytseiniaid: cyfuniadau meddal, cyfuniadau caled ayb

dosbarthu cytseiniaid:
dwywefusol          # bilabial
gwefus-ddeintiol    # labiodental
deintiol            # dental
gorfannol           # alveolar
ffrwydrol           # plosive
"""

# ------------------------------------------------
# lliwiau
# ------------------------------------------------
colormaps = {
    'disglair': {
        "odl": "m",
        "cyfateb": "g",
        "traws": "b",
        "trychben": "r",
        "cysylltben": "r",
        "cyswllt": "y",
        "toriad": "r",
        "pengoll": "y",
        "gwall": "m",
        "amwys": "g",
    }
}

# ------------------------------------------------
# seinegolion
# beth am 'mh', 'nh', 'ngh', 'sh', 'si', 'tsh'
# ------------------------------------------------
ipa_cyts = (
    ('b', 'b'),     # bach, cwbl, mab
    ('d', 'd'),     # dydd, cadw, tad
    ('j', 'dʒ'),    # joio, garej, diengyd
    ('dd', 'ð'),    # ddoe, deuddeg, bedd
    ('ff', 'f'),    # ffenest, ei phen, cyffro, corff
    ('g', 'ɡ'),     # glân, cegin, cig
    ('h', 'h'),     # haul, gwahanol
    ('i', 'j'),     # iaith, geiriadur
    ('c', 'k'),     # cig, acw, ac
    ('l', 'l'),     # leicio, Alban, bol
    ('ll', 'ɬ'),    # llaw, cyllell
    ('m', 'm'),     # mab, cymaint, dim
    ('mh', 'm'),    # fy mhen, ym Mhen-y-bont
    ('n', 'n'),     # nerth, anadlu, gwyn
    ('nh', 'n̥'),    # fy nhad, yn Nhywyn
    ('ng', 'ŋ'),    # fy ngwely, trengi, rhwng
    ('ngh', 'ŋ̊'),   # fy nghŵn, yng Nghymru
    ('p', 'p'),     # pen, copa, map
    ('r', 'r'),     # radio, garw, dŵr
    ('rh', 'r̥'),    # rhestr, anrheg
    ('s', 's'),     # Saesnes, swsus
    ('sh', 'ʃ'),    # siarad, siop, brwsh
    ('si', 'ʃ'),    # siarad, siop, brwsh
    ('t', 't'),     # tatws, at
    ('tsh', 'tʃ'),  # tsieini, wats
    ('th', 'θ'),    # thus, athro, peth
    ('f', 'v'),     # faint, afal, arf
    ('w', 'w'),     # wedyn, ei wraig, gwlân
    ('ch', 'χ'),    # chwaer, tuchan, bwlch
)

ipa_llaf = (
    ('a', 'a'),     # sant, pàs
    ('â', 'aː'),    # mab, sâl
    ('e', 'ɛ'),     # perth, mès
    ('ê', 'eː'),    # peth, trên
    ('y', 'ə'),     # cymydog, rỳg
    ('i', 'ɪ'),     # tipyn, sgìl
    ('u', 'ɨ'),     # punt, gwyn
    ('î', 'iː'),    # hir, tîm
    ('û', 'ɨ'),     # llun, bûm, rhy, tŷ
    ('o', 'ɔ'),     # bron, glòs
    ('ô', 'oː'),    # bro, ôl
    ('w', 'ʊ'),     # cwm, mẁg
    ('ŵ', 'uː'),    # cwch, dŵr
)
ipa_llaf_de = (
    ('î', 'ɪ'),
    ('û', 'iː'),
)

# beth am 'ow', 'ou', 'ey'?
ipa_deus = (
    ('ai', 'ai'),   # tai
    ('au', 'aɨ'),   # cau, nesáu
    ('ae', 'aːɨ'),  # hael, cae
    ('ae', 'aːi'),  # Cymraeg
    ('aw', 'au'),   # llaw
    ('ew', 'ɛu'),   # llew
    ('ei', 'ɛi'),   # reis
    ('eu', 'eɨ'),   # gwneud
    ('yw', 'əu'),   # bywyd
    ('iw', 'ɪu'),   # lliw
    ('uw', 'ɨu'),   # Duw, menyw
    ('oi', 'ɔi'),   # troi
    ('oe', 'ɔɨ'),   # coeden
    ('wy', 'ʊɨ'),   # mwy, gŵyl
)
ipa_deus_de = (
    ('ai', 'ai'),   # tai
    ('au', 'ai'),   # cau, nesáu = tai
    ('ae', 'ai'),   # hael, cae = tai
    ('ae', 'ai'),   # Cymraeg = tai
    ('eu', 'ɛi'),   # gwneud = reis
    ('uw', 'ɪu'),    # duw = lliw
    ('oe', 'ɔi'),   # coeden = troi
    ('wy', 'ʊi'),   # mwy, gwyl = "mwi, gwyil"

)
# symbol prifacen (primary stress)
ipa_prifacen = "ˈ"

# ------------------------------------------------
# nodau
# cytseiniaid: mae angen cynnwys mh, nh, ngh, si, sh, tsh
# ------------------------------------------------
a = ",.'\"\\/!?-;:_@()*^%~{}[]+=|’£–"  # inc. alt-apostrophe
b = "b,c,ch,d,dd,f,ff,g,ng,h,j,l,ll,m,n,p,ph,r,rh,s,t,th,k,q,v,x,z"
b2 = "Ch,Dd,Ff,Ng,Ll,Ph,Rh,Th"
c = "aeiouwy"
d = "âáêéëîïôûúŵẃŷýẙ"
atalnodau = list(a)
cytseiniaid = b.rsplit(",") + b.upper().rsplit(",") + b2.rsplit(",")
llafariaid_byr = list(c + c.upper())
llafariaid_hir = list(d + d.upper())
llafariaid = llafariaid_byr + llafariaid_hir
llythrennau = cytseiniaid + llafariaid

# ------------------------------------------------
# deuseuniaid
# ------------------------------------------------
deuseiniaid = {
    "talgron": ["ia", "ie", "io", "iw", "iy",
                "wa", "we", "wi", "wo", "ua", "yu"],

    "lleddf_cyntaf": ["aw", "ew", "ow", "uw", "yw"],

    "lleddf_ail": ["ae", "ai", "ei", "oe", "oi", "wy"],

    "lleddf_trydydd": ["au", "eu", "ou", "ey", "oy"],

    "deusill": ["uo", "eo", "ea", "oa", "ee", "ao"],

    "eraill": ["ay", "ue", "ya", "uy", "yu", "ye",
               "yo", "wu", "oo", "aa", "iu", "yy", "ui"],
}

dosbarth_deusain = dict(
    [(z, key) for key in deuseiniaid.keys() for z in deuseiniaid[key]]
)
deuseiniaid["lleddf"] = deuseiniaid["lleddf_cyntaf"]
deuseiniaid["lleddf"] += deuseiniaid["lleddf_ail"]
deuseiniaid["lleddf"] += deuseiniaid["lleddf_trydydd"]

# ------------------------------------------------
# llythrenwau
# ------------------------------------------------
llythrenwau = {
    "cynghanedd": {
        "DIM": "Amwys",
        "GWA": "Gwallus",
        # croes
        "CRO": "Croes",
        "COG": "Croes o Gyswllt",
        "CRD": "Croes Drychben",
        "CRG": "Croes Gysylltben",
        # traws
        "TRA": "Traws",
        "TRD": "Traws Drychben",
        "TRG": "Traws Gysylltben",
        # "TRF": "Traws",
        # "TFD": "Traws Drychben",
        # "TFG": "Traws Gysylltben",
        "TRF": "Traws Fantach",
        "TFD": "Traws Fantach Drychben",
        "TFG": "Traws Fantach Gysylltben",
        # llusg
        "LLU": "Llusg",
        "LLL": "Llusg Lafarog",
        "LLD": "Llusg Deirodl",
        # sain
        "SAI": "Sain",
        "SAL": "Sain Lafarog",
        "SOG": "Sain o Gyswllt",
        "SAD": "Sain Drychben",
        "SAG": "Sain Gysylltben",
        "SGA": "Sain Gadwynog",
        "SDO": "Sain Deirodl",
        "SDD": "Sain Ddwbl",
        # cyfansawdd
        "SGR": "Seingroes",
        "SDR": "Seindraws",
        "SLU": "Seinlusg",
        "TGR": "Trawsgroes",
        "TLU": "Trawslusg",
        "CLU": "Croeslusg",
        # pengoll
        "CBG": "Croes Bengoll",
        "TBG": "Traws Bengoll",
    },
    "cydbwysedd": {
        "CYT": "Cytbwys",
        "ANG": "Anghytbwys",
    },
    "acen": {
        "ACE": "Acennog",
        "DIA": "Diacen",
    },
    "aceniad": {
        "CAC": "Cytbwys acennog",
        "CDI": "Cytbwys ddiacen",
        "AAC": "Anghytbwys acennog",
        "ADI": "Anghytbwys ddiacen",
    },
    "odl": {
        "OGY": "Odl gyflawn",
        "OLA": "Odl lafarog",
        "OLU": "Odl lusg gyflawn",
        "OLL": "Odl lusg lafarog",
        "PGY": "Proest gyflawn",
        "PLA": "Proest lafarog",
    },
    "cwpled": {
        "CC7": "Cwpled Cywydd",
        "TOD": "Toddaid",
        "TOB": "Toddaid Byr",
        "TOH": "Toddaid Hir",
        "CYF": "Cyhydedd Fer",
        "CYH": "Cyhydedd Hir",
    },
    "pennill": {
        "EUU": "Englyn Unodl Union",
        "EMI": "Englyn Milwr",
        "EPF": "Englyn Penfyr",
        "CDH": "Cywydd Deuair Hirion",
        "CY9": "Cyhydedd Nawban",
        "BAT": "Byr a Thoddaid",
        "HAT": "Hir a Thoddaid",
    },
    "beiau": {
        "TWY": "Twyll gynghanedd",
        "GOR": "Gormod o odl",
        "PRO": "Proest i'r odl",
        "CRY": "Crych a llyfn",
        "TRW": "Trwm ac ysgafn",
        "LLE": "Lleddf a thalgron",
        "TWO": "Twyll odl",
        "GWE": "Gwestodl",
        "DYB": "Dybryd sain",
        "RHY": "Rhy debyg",
        "YMS": "Ymsathr odlau",
        "HAN": "Hanner proest",
        "CAM": "Camacennu",
        "LLY": "Llysiant llusg",
        "CAG": "Camosodiad gorffwysffa",
        "CAR": "Carnymorddiwes",
        "TIN": "Tin ab",
        "TOR": "Tor mesur",
    },
}

# uchafrifau
max_cytseiniaid_cyswllt = 2
max_cytseiniaid_pengoll = 2

# ------------------------------------------------
# geiriau gwan (AYG tud. 28)
# ------------------------------------------------
geiriau_gwan = [
    # bannod (article)
    "y",
    "yn",
    "yr",
    # rhagenwau (pronouns)
    "fy",
    "dy",
    "di",
    "ei",
    "ein",
    "eich",
    "eu",
    # cysyllteiriau (conjunctions)
    "a",
    "ac", "ag",
    "na", "nac", "nag",
    "neu",
    # bach (sylfaenol)
    "o",
    "o,",
    "i",
    # arddodiadau
    "at",
    "am",
    # eraill
    "yn",
    "yw",
    "yw'r",
    "ar",
    #
    "i'r",
    "a'r",
    "i'w",
    "a'u",
    "a'm",
    "a'i",
    "o'r",
    "O’r",
    "o'i",
    "i'm",
    "i’m",
    "o’r",
    "O’r",
]

# ychwanegu atalnodau (hack)
geiriau_gwan += atalnodau

# ------------------------------------------------
# cyfatebiaeth rhwng llafariaid hir a llafariaid byr
# hir: haf (sillaf ysgafn)
# byr: het (sillaf drom)
# ------------------------------------------------
hir2byr = {
    "â": "a",
    "á": "a",
    "ê": "e",
    "ë": "e",
    "é": "e",
    "î": "i",
    "ï": "i",
    "ô": "o",
    "û": "u",
    "ŵ": "w",
    "ŷ": "y",
    "â".upper(): "A",
    "á".upper(): "A",
    "ê".upper(): "E",
    "ë".upper(): "E",
    "î".upper(): "I",
    "ï".upper(): "I",
    "ô".upper(): "O",
    "û".upper(): "U",
    "ŵ".upper(): "W",
    "ŷ".upper(): "Y",
}

byr2hir = {
    'a': ['â', 'á'],
    'e': ['ê', 'ë', 'é'],
    'i': ['î', 'ï'],
    'o': ['ô'],
    'u': ['û'],
    'w': ['ŵ'],
    'y': ['ŷ'],
}

# ------------------------------------------------
# caledu b -> p, g -> c, d -> t
# ------------------------------------------------
cyfuniadau_caled = {
    #
    ("b", "h"): ("p", "h"),
    ("b", "b"): ("p", "p"),
    ("b", "p"): ("p", "p"),
    ("p", "b"): ("p", "p"),
    #
    ("g", "h"): ("c", "h"),
    ("g", "g"): ("c", "c"),
    ("g", "c"): ("c", "c"),
    ("c", "g"): ("c", "c"),
    #
    ("d", "h"): ("t", "h"),
    ("d", "d"): ("t", "t"),
    ("d", "t"): ("t", "t"),
    ("t", "d"): ("t", "t"),
    #
    ("ff", "f"): ("ff", "ff"),
    ("ff", "f"): ("ff", "ff"),
    ("ll", "l"): ("ll", "ll"),
    # ("l", "ll"): ("ll", "ll"),
    ("th", "dd"): ("th", "th"),
    #
    ("g", "rh"): ("c", "r"),
    ("d", "rh"): ("t", "r"),
    ("b", "rh"): ("p", "r"),
}

# ------------------------------------------------
# meddalu (t -> d, c -> g, p -> b)
# ------------------------------------------------
# cytseiniaid_meddalu = ("c", "ch", "ff", "ll", "p", "s", "th")
# cytseiniaid_meddalu = ("s", "ff", "ch", "c")
cytseiniaid_meddalu = ("s")
cyfatebiaeth_meddal = {
    "t": "d",
    "c": "g",
    "p": "b",
}

# ------------------------------------------------
# cyfuniadau gwyrdro (rhaid i'r ei/eu fod yn yr ail odl)
# ------------------------------------------------
cyfuniadau_gwyrdro = (
    ("aith", "eith"),
    ("ain", "ein"),
    ("aur", "eur"),
    ("au", "eu"),
)

# ------------------------------------------------
# cyfuniadau trychben (trych = truncated, anniben)
# ------------------------------------------------
cyfuniadau_trychben = (
    "br",
    "bl",
    "dr",
    "dl",
    "dn",
    "fl",
    "fn",
    "fr",
    "ffr",
    "ffl",
    "gr",
    "gl",
    "gn",
    "ls",
    "lm",
    "ml",
    "nt",
    "pl",
    "pr",
    "tl",
)

# ------------------------------------------------
# eithriadau (TODO: symud i ffeiliau json)
# ------------------------------------------------
eithriadau = {
    "deusain_ddeusill": (
        "diadell",
        "ddiofryd",
        "dianc",
        "diolch", "ddiolch",
        "dwad",
        "gweddio", "weddio",
        "gweddiwn", "weddiwn",
        "diod", "ddiod",
        "diodydd", "ddiodydd",
        "piod", "biod",
        "priod", "briod", "phriod",
        "priodfab", "briodfab", "phriodfab",
        "priodferch", "briodferch", "phriodferch",
    ),
    "trisain_ddeusill": (
        "gweddiais", "weddiais",
        "rhiain",
        "dywed",
    ),
    "lluosill_acennog": (
        "amen",
        "cangarŵ",
        "cymraeg",
        "dyfalbarhau",
        "ffarwel",
        "iselhau",
        "llawenhau",
        "parhad",
        "ribidires",
        "caerdydd",
        "gyrfaoedd",
        'gadewch',
        'apel',
        'erioed',
        'ymysg',
    ),
    "hir_heb_acen_echblyg": (
        "dyn",
        "ffrwd",
        "hir",
        "rhod",
        "rhwd",
        "tan",
    ),
    "wy_leddf": (
        "dwyn",
        "llwyn",
        "mwyn",
        "nwy",
        "olwyn",
        "plwyf",
        "rhwydd",
        "swyn",
        "trwyn",
    ),
    'w-gytsain': (
        'gwraig', 'wraig', 'ngwraig',
        'gwragedd', 'wragedd',
        'gwlad', 'wlad', 'ngwlad',
        'gwledydd', 'wledydd', 'ngwledydd',
        'gwnaeth', 'wnaeth',
        'gwledd', 'wledd',
        'bedw',
    )
}
