from fastapi import FastAPI

from api.cpe_api.api_functions import check_cpe, get_common_products, mismatched_vendor_names, get_top_100_versions, \
    get_top_10_domains, get_foreign_companies

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "NVD_CPE parser", "version": "0.0.1"}


@app.get("/get_cpe")
async def get_cpe(cpe_string: str):
    return check_cpe(cpe_string)


@app.get("/get_common_products")
async def get_cpe(vendor1: str, vendor2: str):
    return get_common_products(vendor1, vendor2)


@app.get("/mismatched_vendor_names")
async def get_mismatched_vendor_names():
    return mismatched_vendor_names()


@app.get("/top_100_versions")
async def return_top_100_versions():
    return get_top_100_versions()


@app.get("/top_10_domains")
async def return_top_10_domains():
    return get_top_10_domains()


@app.get("/get_foreign_companies")
async def return_foreign_companies():
    return get_foreign_companies()


