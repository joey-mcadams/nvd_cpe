#!/usr/bin/env python3

import os.path
import sys

# Need this to run from the command line
sys.path.append('../')
sys.path.append('./')

from typing import List
from sqlalchemy.orm import Session
from cpe_reader.read_cpe_xml import read_xml
from cpe_parser.parser import CpeParser
from database_engine.model import CPE, CPE23, Reference
from .db_engine import get_engine, setup_metadata
from .magic_hash_function import magic_hash


def populate_database() -> None:
    """
    This function reads the CVE XML input file and populates a local SQL Lite database for further analysis.

    :return: None
    """

    # Clear old data if it's there
    real_path = os.path.dirname(os.path.realpath(__file__))
    db_filename = os.path.join(real_path, "database.db")
    if os.path.isfile(os.path.join(db_filename)):
        os.remove(db_filename)

    # Database setup
    engine = get_engine()
    setup_metadata(engine)

    xml_filename = os.path.join(os.path.dirname(real_path), "official-cpe-dictionary_v2.3.xml")

    xml_root = read_xml(xml_filename)
    print("Done reading XML")

    cpe_parser = CpeParser()
    new_db_entries: List[CPE] = []

    for child in xml_root:
        # TODO: This is dumb, find a better way to do this.
        try:
            cpe_value: str = child.attrib['name']
        except KeyError:
            # This happens with the generate tag. Ignore it
            continue

        cpe_values = cpe_parser.parser(cpe_value)

        if not magic_hash(cpe_values.get("vendor"), "joey"):
            continue

        for grand_child in child:
            # References
            if grand_child.tag == '{http://cpe.mitre.org/dictionary/2.0}references':
                new_references = []
                for reference in grand_child:
                    new_references.append(Reference(title=reference.text, href=reference.attrib["href"]))
                cpe_values["references"] = new_references
            # CPE item
            if grand_child.tag == '{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item':
                # TODO: Remove \ escape chars
                # decoded = grand_child.attrib['name'].encode().decode('unicode_escape')
                cpe23_values = cpe_parser.parser(grand_child.attrib['name'])
                cpe_values["cpe_23"] = CPE23(**cpe23_values)
                continue
            # Title
            if grand_child.tag == '{http://cpe.mitre.org/dictionary/2.0}title':
                cpe_values["title"] = grand_child.text
                continue

        new_cpe: CPE = CPE(**cpe_values)
        new_db_entries.append(new_cpe)

    print("Done parsing XML")

    with Session(engine) as session:
        session.add_all(new_db_entries)
        session.commit()

    print("Done populating database")


# if __name__ == "__main__":
#     populate_database()







