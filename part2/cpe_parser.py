#!/usr/bin/env python3

import sys
import os

from xml.sax.handler import ContentHandler
from xml.sax import parse


# This is bad code, however, the signatures in the spec didn't ask for a file name.
XML_FILENAME = None

class CPEFound(Exception):
    pass


class CPEFinder(ContentHandler):
    def __init__(self, cpe_to_find):
        self.cpe_to_find = cpe_to_find

    def startElement(self, name, attrs):
        if name == "cpe-item":
            cpe_value = attrs.get('name')
            if cpe_value == self.cpe_to_find:
                # couldn't find a better way to do this.
                raise CPEFound("Found cpe-item")

    def endElement(self, name):
        pass

    def characters(self, content):
        pass


class CPECounter(ContentHandler):
    def __init__(self):
        self.cpe_vendor_product_table = {}

    def startElement(self, name, attrs):
        if name == "cpe-item":
            cpe_value = attrs.get('name')
            cpe_split = cpe_value.split(":")
            vendor = cpe_split[2]
            product = cpe_split[3]
            cheap_hash = f"{vendor}:{product}"

            # TODO: Avoid a sort later by inserting in order.
            if cheap_hash in self.cpe_vendor_product_table.keys():
                self.cpe_vendor_product_table[cheap_hash] = self.cpe_vendor_product_table[cheap_hash] + 1
            else:
                self.cpe_vendor_product_table[cheap_hash] = 1

    def endElement(self, name):
        pass

    def characters(self, content):
        pass


def check_cpe(s: str) -> bool:
    """
    Returns `true` if and only if `s` is a CPE in the official XML file.

    :param s:
    :return: boolean if found
    """
    global XML_FILENAME
    if not XML_FILENAME:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        XML_FILENAME = os.path.join(root, "official-cpe-dictionary_v2.2.xml")

    cpe_finder = CPEFinder(s)
    try:
        parse(XML_FILENAME, cpe_finder)
    except CPEFound:
        return True
    return False


def get_top_10_products() -> list[tuple[str, str]]:
    """
    Returns a list of top 10 vendor-product tuples with the most CPEs.

    :return:
    """
    global XML_FILENAME
    if not XML_FILENAME:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        XML_FILENAME = os.path.join(root, "official-cpe-dictionary_v2.2.xml")

    cpe_counter = CPECounter()
    parse(XML_FILENAME, cpe_counter)
    product_dict = cpe_counter.cpe_vendor_product_table
    product_dict_sorted = {k: v for k, v in sorted(product_dict.items(), key=lambda item: item[1], reverse=True)}
    count = 0
    ten_list = []
    for k, v in product_dict_sorted.items():
        if count < 10:
            vendor, product = k.split(":")
            ten_list.append((vendor, product))
            count += 1
        else:
            break

    return ten_list


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cpe_parser.py <cpe_filename>, <check_cpe, get_top_10_products>, <cpe to find>\n"
              "Example: cpe_parser.py get_top_10_products\n"
              "Example: cpe_parser.py check_cpe \"cpe:/a:openafs:openafs:1.6.11.1\"")
        sys.exit(1)

    XML_FILENAME = sys.argv[1]
    function_to_run = sys.argv[2]

    if function_to_run == "check_cpe":
        try:
            cpe_to_find = sys.argv[3]
        except IndexError:
            print("check_cpe requires a cpe to find\n"
                  "Example: cpe_parser.py check_cpe \"cpe:/a:openafs:openafs:1.6.11.1\"")
            sys.exit(1)
        print(f"{check_cpe(cpe_to_find)}")

    if function_to_run == "get_top_10_products":
        print(f"{get_top_10_products()}")

