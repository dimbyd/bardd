# uned.py
'''
Llinell, Cwpled, Pennill neu Cerdd

Er mwyn gwneud pethau sy'n gyffredin i bob un o'r uchod,
e.e. seinegoli, dadansoddi, dangos, 

Dylai hyn berthyn i'r "dadansowddwr" er mwyn gallu storio
dadansoddiadau wrth ymyl y linell, cwpled neu bennill
'''
from bardd.sillaf import Sillaf
from bardd.gair import Gair
from bardd.llinell import Llinell
from bardd.cwpled import Cwpled
from bardd.pennill import Pennill

class Uned():

    def __init__(self, cynnwys=None):

        if not type(cynnwys) in (Gair, Llinell, Cwpled, Pennill, list):
            raise ValueError('Mae angen `Llinell`, `Cwpled` neu `Pennill` fan hyn.')
        
        self.cynnwys = cynnwys


    def geiriau(self):
        '''Echdynnu rhestr geiriau.'''

        # llinell
        if type(self.cynnwys) is Llinell:
            return self.cynnwys.children

        # cwpled
        if type(self.cynnwys) is Cwpled:
            return self.cynnwys.cyntaf.children + self.cynnwys.ail.children
        
        # pennill
        elif type(self.cynnwys) is Pennill:
            geiriau = []
            for uned in Pennill:
                geiriau += uned.geiriau()
            return geiriau

        else:
            raise ValueError("Uned annilys.")

    def sillafau(self):
        '''Echdynnu rhestr sillafau.'''

        sillafau = []

        # gair unigol
        if type(self.cynnwys) is Gair:
            sillafau = self.cynnwys.children

        # llinell
        elif type(self.cynnwys) is Llinell:
            sillafau = [sillaf for gair in self.cynnwys.children for sillaf in gair.children]

        # pennill
        elif type(self.cynnwys) is Pennill:
            sillafau = [gair for llinell in self.cynnwys.children for gair in llinell.children]

        # rhestr geiriau
        elif type(self.cynnwys) in (list, tuple) and all([type(x) is Gair for x in self.cynnwys]):
            sillafau = [sillaf for gair in self.cynnwys for sillaf in gair.children]

        # rhestr sillafau
        elif type(self.cynnwys) in (list, tuple) and all([type(x) is Sillaf for x in self.cynnwys]):
            sillafau = self.cynnwys

        else:
            raise ValueError("Uned annilys.")

        return sillafau
    
    def nifer_sillafau(self):
        return len(self.sillafau())

def main():
    cynnwys = Llinell('O dad yn deulu dedwydd')
    # cynnwys = Gair('bamboozle')
    uned = Uned(cynnwys)
    print(uned.sillafau())
    print(uned.nifer_sillafau())
    print(uned.geiriau())


if __name__ == "__main__":
    main()
