import os
import time

from sqlalchemy.orm import Session

from .db_engine import get_engine, setup_metadata
from .model import CPE23, CPE


def test_add_cpe():
    engine = get_engine()
    setup_metadata(engine)

    test_cpe_23 = CPE23(
        name="test",
        part="a",
        vendor="adobe",
        product="photoshop",
        version="*",
        update="beta",
        edition="windows",
        language="US/EN",
        sw_edition="windows",
        target_sw="windows",
        target_hw="intel",
        other=None,
    )

    test_cpe = CPE(
        name="test",
        title="test_title",
        part="a",
        vendor="adobe",
        product="photoshop",
        version="*",
        update="beta",
        edition="windows",
        language="US/EN",
        cpe_23=test_cpe_23,
    )

    with Session(engine) as session:
        session.add(test_cpe)
        session.commit()
