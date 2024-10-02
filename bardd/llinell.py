# llinell.py

from bardd.base import TreeNode
from bardd.gair import Gair

class Llinell(TreeNode):
    """
    Dosbarth i ddarlunio llinell fel rhestr geiriau
    """

    def __init__(self, s, awdur=None, parent=None):
        TreeNode.__init__(self, parent=parent)

        # creu rhestr geiriau (hollti ar fylchau)
        if type(s) is str:
            s = s.strip()
            self.children = [Gair(sg) for sg in s.split(" ")]

        elif type(s) is list and all([type(x) is Gair for x in s]):
            self.children = s

        else:
            self.children = None

    def __str__(self):
        return " ".join([str(gair) for gair in self.children])

    def __repr__(self):
        return " ".join([repr(gair) for gair in self.children])

    def sain(self):
        return " ".join([gair.sain() for gair in self.children])

    def geiriau(self):
        return self.children

    def prifodl(self):
        if self.children:
            return self.children[-1]
        return None

    def llinyn(self):
        return " ".join([str(gair) for gair in self.children])

    def llinyn_acenion(self):
        return " ".join([g.llinyn_acenion() for g in self.children])

    def llinyn_cytseiniaid(self):
        return " ".join([g.llinyn_cytseiniaid() for g in self.children])

    def llinyn_llafariaid(self):
        return " ".join([g.llinyn_llafariaid() for g in self.children])

    # stats
    def nifer_geiriau(self):
        return len(self.children)

    def nifer_sillafau(self):
        return sum([g.nifer_sillafau() for g in self.children])


# ------------------------------------------------
def main():

    from bardd.data_llinellau import profion

    for key in [
        # "croes",
        # "croes_o_gyswllt",
        # "traws",
        # "llusg",
        # "llusg_lafarog",
        # "llusg_odl_gudd",
        # "llusg_odl_ewinog",
        # "sain",
        # "sain_odl_gudd",
        # "sain_odl_ewinog",
        # "sain_lafarog",
        # "sain_o_gyswllt",
        # "sain_gadwynog",
        # 'trychben',
        # 'cysylltben',
        # 'seingroes',
        # 'trawsgroes',
        # 'seindraws',
        # 'croeslusg',
        # 'seinlusg',
        # 'trawslusg',
        # 'misc',
        # 'sain_siwr',
        'test',
    ]:
        # call(["clear"])
        print("==============================")
        print(key.upper())
        print("==============================")
        for s in profion[key]:
            print(s)
            ll = Llinell(s)
            print(ll.llinyn_acenion())
            print(ll.llinyn())
            print(ll.llinyn_cytseiniaid())
            print(ll.sain())
            print()
        # try:
        #     input(">> bwrwch y dychwelwr i barhau ...")
        # except KeyboardInterrupt:
        #     print("Beth?")
        #     return


if __name__ == "__main__":
    main()
