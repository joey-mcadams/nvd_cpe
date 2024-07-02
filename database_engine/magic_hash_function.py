import hashlib


def magic_hash(vendor: str, person_name="joey") -> bool:
    """
    Return true if the first hex value of the vendor and the person name are the same.

    :param vendor: string
    :param person_name: string
    :return: bool
    """
    if vendor is None:
        raise ValueError("Vendor cannot be None")

    sha1 = hashlib.sha1()
    sha1.update(bytes(vendor, encoding="utf"))
    first_letter_v = sha1.hexdigest()

    sha1 = hashlib.sha1()
    sha1.update(bytes(person_name, encoding="utf"))
    first_letter_p = sha1.hexdigest()

    return first_letter_v[0] == first_letter_p[0]