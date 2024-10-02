# demo.py

from subprocess import call
from bardd.llinell import Llinell

# data
llinellau = {
    "croes": (
        "Ochain cloch a chanu clir",
        "Si'r oerwynt a sêr araul",
        "Awdur mad a dramodydd",
        "Ei awen brudd yn eu bro",
        "Onid teg yw ein tud?",
    ),
    "croes_o_gyswllt": (
        "Aderyn llwyd ar un llaw",
        "Daw geiriau Duw o'i gaer deg",
        "Rhwydd gamwr, hawdd ei gymell",
        "Gwr enwog yw o ran gwaith",  # methiant
    ),
    "traws": (
        "Ochain cloch a gwreichion clir",
        "Si'r oerwynt dan sêr araul",
        "Awdur mad yw'r dramodydd",
        "Ei awen brudd dros ein bro",
        "Ni all lladd ond ennyn llid",
    ),
    "traws_fantach": (
        "Y gŵr aruchel ei gân",
        "Y brawd o bellafion bro",
        "Brwd yw aderyn brig",
        "Glaw ar ymylon y glyn",
    ),
    "llusg": (
        "Beiddgar yw geiriau cariad",
        "Y mae arogl yn goglais",
        "Pell ydyw coed yr ellyll",
        "Y mae Morfudd yn cuddio",
        "Yr haul ar dawel heli",
        "Taw â'th sôn, gad fi'n llonydd",
        "Ymysg y bedw yn ddedwydd",  # methiant
    ),
    "llusg_lafarog": (
        "Un distaw ei wrandawiad",
        "Gwynt y rhew yn distewi",
    ),
    "llusg_odl_gudd": (
        "Ac yma bu cydnabod",
        "Ac wedi d'awr godidog",
        "Ac wele lid y gelyn",
        "Gwn ddifa lawer calon",
        "Eto dring lethr Carn Ingli",
        "Y ddinas draw yn wastraff",
        "Esgor mae llid ar ormes",
        "Bu llawer ddoe yn cerdded",
        "Dacw wiw dyfiant liwdeg",
        "Ac wele wychder Dewi",
    ),
    "llusg_odl_ewinog": (
        "Yn wyneb haul ar Epynt",
        "Yr esgob biau popeth",
        "Aeth fy nghariad hyd ato",
        "O'r garreg hon daeth eco",
        "I'r esgob pur rhoed popeth",
        "Fy nghariad troaf atat",
        "O'r garreg clywaid eco",
    ),
    "sain": (
        "Cân ddiddig ar frig y fron",
        "Gŵr amhur yn sur ei sen",
        "Bydd y dolydd yn deilio",
        "Canlyniad cariad yw cosb",
        "Cân hardd croyw fardd Caerfyrddin",
        "Mae'n gas gennyf dras y dref",
        "Heddychwr gwr rhagorol",
    ),
    "sain_odl_ewinog": (
        "Caf fynd draw ar hynt i'r rhos",
        "Rhoi het ar ei harffed hi",
        "Caf fynd tua'r helynt draw",
    ),
    "sain_odl_gudd": (
        "Eu plaid yw duw rhai drwy'u hoes",
        "Llyfrdra dy wlad nid yw les",
        "A'i gord yn deffro'r dyffryn",
        "Aeth Idris draw'n drist gan drawster",
        "Nid â dy gariad o gof",
    ),
    "sain_lafarog": (
        "Fe ddaeth pob croes i'w oes ef",
        "Didranc ieuanc ei awen",
        "Pren gwyrddliw o wiw wead",
        "Gŵr o ystryw ydyw ef",
    ),
    "sain_o_gyswllt": (
        "Galarnad groch a chloch leddf",
        "Bydd sug i'r grug a'r egin",
        "Dy fab rhad O! Dad yw ef",  # methiant
    ),
    "sain_gadwynog": (
        "Dringo bryn a rhodio bro",
        "Trydar mwyn adar y mynydd",
        "Un dydd gwelais brydydd gwiw",
    ),
    "trychben": (
        "Canu mydr cyn ymadael",
        "Nid yn aml y down yma",
        "Ond daw gwefr cyn atgofion",
        "Calon ddofn ei hofn hefyd",
        "Parabl anabl anniben",  # methiant: cam-acennu "anabl"
    ),
    "cysylltben": (
        "Onid bro dy baradwys",
        "Yma bu nwyf i'm beunydd",
        "Mawl ar daen gwae nid gweniaith",
        "A ddaw fy mab i Ddyfed",
    ),
    "seingroes": (
        "Y cawr mawr yn curo myrdd",
        "Lleuad fad lleuad fedi",
        "Gweled cur o glywed can",
        "Eos dlos yn deilio ir",
    ),
    "trawsgroes": (
        "Enaid unig a dinam",
        "Geiriau gwrol gor-gywrain",
    ),
    "seindraws": (
        "Y feinwen fwynwen fanwallt",
        "Gwrol gwrol frawdgarwch",
    ),
    "croeslusg": (
        "Duw ei hun a'u dihunodd",
        "Ein ceidwad eon cadarn",
    ),
    "seinlusg": (
        "Gwyraf, yfaf o'r afon",
        "Gŵr o forwr a fwriwyd",
    ),
    "trawslusg": (
        "Y feinwen a gâr f'enaid",
        "Yr arwr mewn arwriaeth",
    ),
    "misc": (
        "Eithin aur a hithau'n haf",
        "Arian ac aur yn ei god",
        "A phur yw pob offeren",
        "Deued dydd o wrando taer",
        "Ym mhob byw y mae pawen",
        "Ac ar ffin y gorffenol",
    ),
}


def run_demo(verbose=True):
    for key in [
        "croes",
        "croes_o_gyswllt",
        "traws",
        "traws_fantach",
        "llusg",
        "llusg_lafarog",
        "llusg_odl_gudd",
        "llusg_odl_ewinog",
        "sain",
        "sain_odl_gudd",
        "sain_odl_ewinog",
        "sain_lafarog",
        "sain_o_gyswllt",
        "sain_gadwynog",
        "trychben",
        "cysylltben",
        "seingroes",
        # 'trawsgroes',
        "seindraws",
        "croeslusg",
        "seinlusg",
        "trawslusg",
    ]:
        call(["clear"])
        print("==============================")
        print(key.upper())
        print("==============================")
        for s in llinellau[key]:
            dad = Llinell(s).dadansoddiad()
            print(dad)
        try:
            input(">> bwrwch y dychwelwr i barhau ...")
        except KeyboardInterrupt:
            print
            return


def main():
    run_demo()


if __name__ == "__main__":
    main()
