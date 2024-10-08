# cyfres.py
"""
Dosbarth i fynegi cyfres o nodau.
"""

from bardd.base import TreeNode
from bardd.nod import Nod

import logging
log = logging.getLogger(__name__)


class Cyfres(TreeNode):
    """
    Cyfres o nodau yn cynnwys atalnodau
    Caiff deugraffau eu prosesu yma
    """

    def __init__(self, s="", parent=None):
        """
        Creu cyfres nodau o linyn elfennol
        """
        TreeNode.__init__(self, parent=parent)

        # cyfres wag
        if not s:
            self.children = []

        # creu cyfres allan o restr nodau
        elif type(s) in (list, tuple) and all([type(a) is Nod for a in s]):
            self.children = s

        # creu cyfres allan o gyfres
        elif type(s) is Cyfres:
            self.children = s.children

        # creu o `str`
        elif type(s) is str:
            self.children = []
            idx = 0
            while idx < len(s):
                
                # echdynn'r symbol (unicode)
                c = s[idx]

                # gwirio am ddeugraffau
                if (
                    c.lower() in ["c", "d", "f", "n", "l", "p", "r", "t"]
                    and idx < len(s) - 1
                ):
                    c_nesaf = s[idx + 1]

                    if c.lower() == "c" and c_nesaf == "h":
                        self.children.append(Nod(c + "h"))
                        idx += 1
                    elif c.lower() == "d" and c_nesaf == "d":
                        self.children.append(Nod(c + "d"))
                        idx += 1
                    elif c.lower() == "f" and c_nesaf == "f":
                        self.children.append(Nod(c + "f"))
                        idx += 1
                    elif c.lower() == "n" and c_nesaf == "g":
                        self.children.append(Nod(c + "g"))
                        idx += 1
                    elif c.lower() == "l" and c_nesaf == "l":
                        self.children.append(Nod(c + "l"))
                        idx += 1
                    elif c.lower() == "p" and c_nesaf == "h":
                        self.children.append(Nod(c + "h"))
                        idx += 1
                    elif c.lower() == "r" and c_nesaf == "h":
                        self.children.append(Nod(c + "h"))
                        idx += 1
                    elif c.lower() == "t" and c_nesaf == "h":
                        self.children.append(Nod(c + "h"))
                        idx += 1
                    else:
                        self.children.append(Nod(c))

                else:
                    self.children.append(Nod(c))
                idx += 1
        else:
            raise ValueError(
                "Wedi methu creu gwrthrych `Cyfres` o'r mewnbwn {}".format(s)
            )

    def __eq__(self, other):
        return (
            isinstance(other, Cyfres)
            and len(self.children) == len(other.children)
            and all([a.text == b.text for a, b in zip(self.children, other.children)])
        )

    def __len__(self):
        return len(self.children)

    def __add__(self, other):
        if isinstance(other, Cyfres):
            return Cyfres(self.children + other.children)
        return ()

    def __str__(self):
        return "".join([nod.text for nod in self.children])

    def __repr__(self):
        return "".join([nod.text for nod in self.children])

    def __setitem__(self, idx, data):
        self.children[idx] = data

    def __getitem__(self, idx):
        return self.children[idx]

    def sain(self):
        return ''.join([nod.sain for nod in self.children])

    def gwag(self):
        return not len(self.children) > 0

    def hyd(self):
        return len(self.children)

    def byr(self):
        return "".join([nod.byr() for nod in self.children])

    def bychan(self):
        return "".join([nod.bychan() for nod in self.children])

    def nodau(self):
        return self.children

    def llafariaid(self, atalnodau=False):
        if atalnodau:
            nodau = [nod for nod in self.children if nod.is_llafariad() or nod.is_atalnod()]
        else:
            nodau = [nod for nod in self.children if nod.is_llafariad()]
        return Cyfres(nodau)

    def cytseiniaid(self, atalnodau=False):
        if atalnodau:
            nodau = [nod for nod in self.children if nod.is_cytsain() or nod.is_atalnod()]
        else:
            nodau = [nod for nod in self.children if nod.is_cytsain()]
        return Cyfres(nodau)


# ------------------------------------------------
# test
def main():

    s = 'anifeiliaid'
    s = 'cystrawen'
    cyf = Cyfres(s)
    print(cyf)
    print(cyf.children)

    print(cyf[2])
    print(type(cyf[2]))


if __name__ == "__main__":
    main()
