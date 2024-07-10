from api.cpe_parser import CpeParser


def test_parse_cpe():
    test_string = "cpe:/a:%240.99_kindle_books_project:%240.99_kindle_books:6::~~~android~~"
    cpe = CpeParser()
    output = cpe.parser(test_string)

    assert output == {'edition': '~~~android~~',
                      'name': 'cpe:/a:%240.99_kindle_books_project:%240.99_kindle_books:6::~~~android~~',
                      'part': 'a',
                      'product': '$0.99_kindle_books',
                      'update': '',
                      'vendor': '$0.99_kindle_books_project',
                      'version': '6'}


def test_parse_cpe23():
    test_string = "cpe:2.3:a:\@thi.ng\/egf_project:\@thi.ng\/egf:-:*:*:*:*:node.js:*:*"
    cpe = CpeParser()
    output = cpe.parser(test_string)

    assert output == {'edition': '*',
                      'language': '*',
                      'name': 'cpe:2.3:a:\\@thi.ng\\/egf_project:\\@thi.ng\\/egf:-:*:*:*:*:node.js:*:*',
                      'other': '*',
                      'part': 'a',
                      'product': '\\@thi.ng\\/egf',
                      'sw_edition': '*',
                      'target_hw': '*',
                      'target_sw': 'node.js',
                      'update': '*',
                      'vendor': '@thi.ng/egf_project',
                      'version': '-'}