import os

from sqlalchemy import create_engine, Engine

from database_engine.model import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

def get_engine() -> Engine:
    return create_engine(f'sqlite:///{db_path}')


def setup_metadata(engine: Engine) -> None:
    Base.metadata.create_all(engine)