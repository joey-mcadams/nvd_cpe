from typing import List, Optional

from pydantic import BaseModel


class PyCPE23(BaseModel):
    name: str
    part: str
    vendor: str
    product: str
    version: str
    update: Optional[str] = None
    edition: Optional[str] = None
    language: Optional[str] = None
    sw_edition: Optional[str] = None
    target_sw: Optional[str] = None
    target_hw: Optional[str] = None
    other: Optional[str] = None


class PyReference(BaseModel):
    href: str
    title: str


class PyCPE(BaseModel):
    name: str
    title: str
    part: str
    vendor: str
    product: str
    version: str
    update: Optional[str] = None
    edition: Optional[str] = None
    language: Optional[str] = None
    sw_edition: Optional[str] = None
    target_sw: Optional[str] = None
    target_hw: Optional[str] = None
    other: Optional[str] = None
    cpe_23: Optional[PyCPE23] = None
    references: Optional[List[PyReference]] = None


