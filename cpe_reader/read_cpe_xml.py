import xml
import xml.etree.ElementTree as ET


def read_xml(filename: str) -> xml.etree.ElementTree:
    """
    Read the xml NVD CPE input and return the root of the tree

    :return: ElementTree
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    return root




