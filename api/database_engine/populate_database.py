#!/usr/bin/env python3

import os.path

from api.database_engine.pydantic_layer.pydantic_models import PyReference, PyCPE23, PyCPE
from api.database_engine.pydantic_layer.translate_model import translate_pydantic_cpe_to_sqlalchemy

from typing import List
from sqlalchemy.orm import Session
from api.cpe_reader.read_cpe_xml import read_xml
from api.cpe_parser import CpeParser
from api.database_engine.model import CPE
from api.database_engine.db_engine import get_engine, setup_metadata
from api.database_engine.magic_hash_function import magic_hash


def initialize_and_populate_database(remove_existing_database: bool = True) -> None:
    """
    This function reads
     the CVE XML input file and populates a local SQL Lite database for further analysis.

    :return: None
    """
    real_path = os.path.dirname(os.path.realpath(__file__))

    # Clear old data if it's there
    if remove_existing_database:
        db_filename = os.path.join(real_path, "database.db")
        if os.path.isfile(db_filename):
            os.remove(db_filename)

    # Database setup
    engine = get_engine()
    setup_metadata(engine)

    # Go up two and read the XML file from the root.
    xml_filename = os.path.join(os.path.dirname(os.path.dirname(real_path)), "official-cpe-dictionary_v2.3.xml")

    xml_root = read_xml(xml_filename)
    print("Done reading XML")

    new_db_entries: List[CPE] = []
    parse_xml_object(new_db_entries, xml_root)
    print("Done parsing XML")

    with Session(engine) as session:
        session.add_all(new_db_entries)
        session.commit()
    print("Done populating database")


def parse_xml_object(new_db_entries, xml_root):
    cpe_parser = CpeParser()
    for child in xml_root:
        if child.tag != "{http://cpe.mitre.org/dictionary/2.0}cpe-item":
            continue

        cpe_value: str = child.attrib['name']
        cpe_values = cpe_parser.parser(cpe_value)

        if not magic_hash(cpe_values.get("vendor"), "joey"):
            continue

        for grand_child in child:
            # References
            if grand_child.tag == '{http://cpe.mitre.org/dictionary/2.0}references':
                new_references = []
                for reference in grand_child:
                    new_references.append(PyReference(title=reference.text, href=reference.attrib["href"]))
                cpe_values["references"] = new_references

            # CPE item
            if grand_child.tag == '{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item':
                cpe23_values = cpe_parser.parser(grand_child.attrib['name'])
                cpe_values["cpe_23"] = PyCPE23(**cpe23_values)
                continue

            # Title
            if grand_child.tag == '{http://cpe.mitre.org/dictionary/2.0}title':
                cpe_values["title"] = grand_child.text
                continue

        new_cpe: CPE = translate_pydantic_cpe_to_sqlalchemy(PyCPE(**cpe_values))
        new_db_entries.append(new_cpe)
