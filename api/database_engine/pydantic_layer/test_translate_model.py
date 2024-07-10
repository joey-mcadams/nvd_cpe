from api.cpe_parser import CpeParser
from database_engine.model import CPE
from database_engine.pydantic_layer.pydantic_models import PyReference, PyCPE23, PyCPE
from database_engine.pydantic_layer.translate_model import translate_pydantic_cpe_to_sqlalchemy


def test_translate_pydantic_cpe_to_sqlalchemy():
    test_cpe23_string = "cpe:2.3:a:\@thi.ng\/egf_project:\@thi.ng\/egf:-:*:*:*:*:node.js:*:*"
    test_cpe_string = "cpe:2.3:a:\@thi.ng\/egf_project:\@thi.ng\/egf:-"
    cpe = CpeParser()
    cpe_23_attribs = cpe.parser(test_cpe23_string)
    cpe_attribs = cpe.parser(test_cpe_string)
    
    py_cpe_23 = PyCPE23(**cpe_23_attribs)
    py_references = [
        PyReference(href="http://www.google.com", title="Google"),
        PyReference(href="http://www.bing.com", title="Bing")
    ]
    
    cpe_attribs["cpe_23"] = PyCPE23(**cpe_23_attribs)
    cpe_attribs["references"] = py_references
    cpe_attribs["title"] = "A Super Product"
    py_cpe= PyCPE(**cpe_attribs)
    
    result = translate_pydantic_cpe_to_sqlalchemy(py_cpe)
    assert isinstance(result, CPE)
