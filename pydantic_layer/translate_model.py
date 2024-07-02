from database_engine.model import CPE, CPE23, Reference
from pydantic_layer.pydantic_models import PyCPE


def translate_pydantic_cpe_to_sqlalchemy(py_cpe: PyCPE) -> CPE:
    """
    This will tranlate a Pydantic model to a SQLAlchemy model.

    :return: SQLAlchemy CPE model
    """
    attributes = py_cpe.__dict__

    attributes['cpe_23'] = CPE23(**attributes['cpe_23'].__dict__)

    new_references = []

    if 'references' in attributes.keys() and attributes['references'] is not None:
        for r in attributes['references']:
            new_references.append(Reference(**r.__dict__))

    attributes['references'] = new_references

    return CPE(**attributes)
