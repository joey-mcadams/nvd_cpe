from part2.cpe_parser import check_cpe, get_top_10_products, XML_FILENAME


def test_check_cpe():
    test_cpe = "cpe:/a:openafs:openafs:1.5.60"

    result = check_cpe(test_cpe)
    assert result

    result = check_cpe("No find me")
    assert not result


def test_get_top_10_products():
    result = get_top_10_products()
    assert len(result) == 10