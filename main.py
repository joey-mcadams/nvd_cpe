#/bin/bash python3

import part2.cpe_parser
import os
from cpe_api.api_functions import check_cpe, get_common_products, mismatched_vendor_names, get_top_100_versions, \
    get_top_10_domains, get_foreign_companies
from database_engine.populate_database import populate_database

# Clear data if it exists.
real_path = os.path.dirname(os.path.realpath(__file__))
db_filename = os.path.join(real_path + "/database_engine/database.db")
if os.path.isfile(os.path.join(real_path + "/database_engine/database.db")):
    os.remove(db_filename)

print("*******************************")
print("Part 1:")
print("*******************************")

print("* Populate Database w/ Magic Hash")
populate_database()

print("* check_cpe(s: str) -> bool : checking for cpe:2.3:a:darwin:factor:1.3.3:*:*:*:*:node.js:*:*")
print(check_cpe("cpe:2.3:a:darwin:factor:1.3.3:*:*:*:*:node.js:*:*"))

print("* get_common_products(vendor1: str, vendor2: str) -> list[str] : znc - znc")
print(get_common_products("znc", "znc"))

print("* mismatched_vendor_names() : This will return an empty list.")
print(mismatched_vendor_names())

print("* get_top_100_versions() -> list[tuple[str, int]]")
print(get_top_100_versions())

print("* get_top_10_domains() -> list[str]")
print(get_top_10_domains())

print("* get_foreign_companies() -> int")
print(get_foreign_companies())

print("*******************************")
print("Part 2:")
print("*******************************")

print("* check_cpe(s: str) -> bool : cpe:/a:%5bgwa%5d_autoresponder_project:%5bgwa%5d_autoresponder:-::~~~wordpress~~")
print(part2.cpe_parser.check_cpe("cpe:/a:%5bgwa%5d_autoresponder_project:%5bgwa%5d_autoresponder:-::~~~wordpress~~"))
print("* get_top_10_products() -> list[tuple[str, str]]")
print(part2.cpe_parser.get_top_10_products())