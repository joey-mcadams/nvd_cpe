from operator import itemgetter

from sqlalchemy import func, desc, distinct, select, text
from sqlalchemy.orm import Session

from database_engine.model import CPE
from database_engine.db_engine import get_engine


def check_cpe(s: str) -> bool:
    """
    Check if a CPE exists. Not an exact match

    :param s: String to search for
    :return:
    """
    engine = get_engine()

    with Session(engine) as session:
        result = session.query(CPE).filter(CPE.name.is_(s)).count()

    if result:
        return True

    return False


def get_common_products(vendor1: str, vendor2: str) -> list:
    """
    Returns a list of products common across two vendors.

    :param vendor1: Vendor Name (String)
    :param vendor2: Vendor Name (String)
    :return: List of Products
    """
    engine = get_engine()
    common_products = []

    with Session(engine) as session:
        vendor1_entries = session.query(CPE).with_entities(CPE.product).filter(CPE.vendor.is_(vendor1)).all()
        vendor2_entries = session.query(CPE).with_entities(CPE.product).filter(CPE.vendor.is_(vendor2)).all()

    unified_list = list(set(vendor1_entries) & set(vendor2_entries))
    output = [x[0] for x in unified_list]
    return output


def mismatched_vendor_names() -> list[tuple[str, str]]:
    """
    Returns a list of tuple of vendor names that differ in their CPE 2.2 and CPE 2.3 strings.

    :return: List of tuples with mismatched vendor names.
    """
    engine = get_engine()
    all_results = []
    with Session(engine) as session:
        all_cpe = session.query(CPE).all()
        for cpe in all_cpe:
            vendor1 = cpe.vendor
            vendor2 = cpe.cpe_23.vendor.replace('\\', '')
            if vendor1 != vendor2:
                all_results.append((vendor1, vendor2))

    return all_results


def get_top_100_versions() -> list[tuple[str, int]]:
    """
    Returns a sorted list of 100 most popular versions and their count, regardless of vendors or products.

    :return: list of tuples with (version, count)
    """
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version, COUNT(*) AS `num` FROM cpe_item GROUP BY version")).all()

    results = result
    results.sort(key=itemgetter(1), reverse=True)
    return results[:100]


def get_top_10_domains() -> list[str]:
    """
    Returns a list of most popular domains used in references.

    :return: List of domains
    """
    sql_command = """
SELECT
  SUBSTR(SUBSTR(href, INSTR(href, '//') + 2), 0, INSTR(SUBSTR(href, INSTR(href, '//') + 2), '/')) AS domain,
  Count(*) AS num_hits
FROM reference_item GROUP BY domain;
"""

    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text(sql_command)).all()

    results = result
    results.sort(key=itemgetter(1), reverse=True)
    results = results[:10]
    domains = [x[0] for x in results]
    return domains


def get_foreign_companies() -> int:
    """
    Returns the number of vendors or products with non-ASCII Unicode characters in their title.

    :return:
    """
    engine = get_engine()
    with engine.connect() as connection:
        results = connection.execute(text("SELECT vendor, product, title FROM cpe_item")).all()

    count = 0

    for result in results:
        if not result[2].isascii():
            count += 1

    return count

