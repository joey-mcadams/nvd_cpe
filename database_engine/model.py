from typing import List, Optional

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Reference(Base):
    __tablename__ = 'reference_item'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    href: Mapped[str]
    title: Mapped[str]
    parent_id = mapped_column(ForeignKey("cpe_item.name"))
    parent: Mapped["CPE"] = relationship(back_populates="references")

    def __repr__(self):
        return f"{self.title} - {self.href}"


class CPE(Base):
    __tablename__ = "cpe_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    part: Mapped[Optional[str]]
    vendor: Mapped[Optional[str]]
    product: Mapped[Optional[str]]
    version: Mapped[Optional[str]]
    update: Mapped[Optional[str]]
    edition: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    sw_edition: Mapped[Optional[str]]
    target_sw: Mapped[Optional[str]]
    target_hw: Mapped[Optional[str]]
    other: Mapped[Optional[str]]
    cpe_23_id: Mapped[int] = mapped_column(ForeignKey("cpe_23_item.id"))
    cpe_23: Mapped[Optional["CPE23"]] = relationship(back_populates="parent")
    references: Mapped[List["Reference"]] = relationship(back_populates="parent")

    def __repr__(self):
        return self.name


class CPE23(Base):
    __tablename__ = 'cpe_23_item'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]]
    part: Mapped[Optional[str]]
    vendor: Mapped[Optional[str]]
    product: Mapped[Optional[str]]
    version: Mapped[Optional[str]]
    update: Mapped[Optional[str]]
    edition: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    sw_edition: Mapped[Optional[str]]
    target_sw: Mapped[Optional[str]]
    target_hw: Mapped[Optional[str]]
    other: Mapped[Optional[str]]
    parent: Mapped["CPE"] = relationship(back_populates="cpe_23")

    def __repr__(self):
        return self.name
