"""
Base class for lexical units.
"""

from lxml import etree


class TreeNode(object):
    """
    Abstract class for Nod, Sillaf, Gair, Llinell, Cwpled, Pennill, Cerdd.
    """

    # class variable
    counter = 0

    def __init__(self, parent=None):
        TreeNode.counter += 1
        self.node_id = TreeNode.counter
        self.parent = parent
        self.children = []

    def __str__(self):
        return "".join([str(child) for child in self.children])

    def __repr__(self):
        return "".join([repr(child) for child in self.children])

    def xml(self):
        element_name = self.__class__.__name__.lower()
        element = etree.Element(element_name)

        # recursive call
        for child in self.children:
            child_element = child.xml()  # The `Nod` subclass outputs text here
            element.append(child_element)
        return element

        # set element text
        # if not self.children and self.text:
        # if hasattr(self, 'text') and self.text:
        #     element.text = self.text.strip()


# ------------------------------------------------
def main():
    node = TreeNode()
    child = TreeNode()
    node.children.append(child)
    xml_tree = node.xml()
    xstr = etree.tostring(xml_tree, pretty_print=True).decode("utf-8")
    print(xstr)


if __name__ == "__main__":
    main()
