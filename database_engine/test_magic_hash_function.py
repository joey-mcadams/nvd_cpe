from magic_hash_function import magic_hash


def test_magic_hash():
    result = magic_hash("joey", "joey")
    assert result

    result = magic_hash("not_joey", "joey")
    assert not result

    result = magic_hash("j", "joey")
    assert result

    result = magic_hash("07fly", "joey")
    assert result
