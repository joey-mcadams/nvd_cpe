from math import floor
from random import randrange

import api.cpe_api.api_functions as api_functions

from sqlalchemy.orm import Session
from unittest import TestCase, mock
from sqlalchemy import create_engine, Engine
from api.cpe_parser import CpeParser
from api.database_engine.model import Base, CPE, CPE23, Reference


class TestAPIFunctions(TestCase):
    def setUp(self) -> None:
        """
        Create a new test database
        """
        self.engine = create_engine(f'sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)

        # Create data here
        # This would be easier with a test factory of some sort, but I wasn't sure
        # if that's allowed due to the constraints of the test.
        new_fake_cpe_list = []
        cpe_parser = CpeParser()

        # Base CPE
        fake_cpe_data = cpe_parser.parser("cpe:/o:hp:j6u57a_firmware:001.1937d")
        fake_cpe_data['title'] = "Some super cool vulnerability."
        test_cpe = CPE(**fake_cpe_data)
        fake_cpe32_data = cpe_parser.parser("cpe:2.3:o:hp:j6u57a_firmware:001.1937d:*:*:*:*:*:*:*")
        test_cpe.cpe_23 = CPE23(**fake_cpe32_data)
        new_fake_cpe_list.append(test_cpe)

        # Base CPE duplicate product
        fake_cpe_data = cpe_parser.parser("cpe:/o:some_other_vendor:j6u57a_firmware:001.1937d")
        fake_cpe_data['title'] = "Some super cool vulnerability."
        test_cpe = CPE(**fake_cpe_data)
        fake_cpe32_data = cpe_parser.parser("cpe:2.3:o:some_other_vendor:j6u57a_firmware:001.1937d:*:*:*:*:*:*:*")
        test_cpe.cpe_23 = CPE23(**fake_cpe32_data)
        new_fake_cpe_list.append(test_cpe)

        # Put in lots of data
        for count in range(1000):
            rand_version = floor(count / (randrange(5) + 1))
            fake_cpe_data = cpe_parser.parser(f"cpe:/o:hp{count}:j6u57a_firmware{count}:{rand_version}.001.1937d")
            fake_cpe_data['title'] = f"Some super cool vulnerability - {count}"
            test_cpe = CPE(**fake_cpe_data)
            fake_cpe32_data = cpe_parser.parser(f"cpe:2.3:o:hp{count}:j6u57a_firmware{count}:{rand_version}.001.1937d:*:*:*:*:*:*:*")
            test_cpe.cpe_23 = CPE23(**fake_cpe32_data)
            fake_domain = f"http://www.{count % 10}domain.com/"
            fake_title = "fake_domain"
            reference = Reference(href=fake_domain, title=fake_title)
            test_cpe.references = [reference]
            new_fake_cpe_list.append(test_cpe)

        # Mismatched Vendor
        fake_cpe32_data = cpe_parser.parser("cpe:2.3:o:microsoft:j6u57a_firmware:001.1937d:*:*:*:*:*:*:*")
        test_cpe_23 = CPE23(**fake_cpe32_data)
        fake_cpe_data = cpe_parser.parser("cpe:/o:micro\\$oft:j6u57a_firmware:001.1937d")
        fake_cpe_data['title'] = "Some super cool vulnerability."
        fake_cpe_data["cpe_23"] = test_cpe_23
        test_cpe = CPE(**fake_cpe_data)
        new_fake_cpe_list.append(test_cpe)

        # Foreign Chars
        fake_cpe32_data = cpe_parser.parser("cpe:2.3:o:hp龙:j6u57a_firmware:001.1937d:*:*:*:*:*:*:*")
        test_cpe_23 = CPE23(**fake_cpe32_data)
        fake_cpe_data = cpe_parser.parser("cpe:/o:hp:j6u57a_firmware:001.1937d")
        fake_cpe_data["cpe_23"] = test_cpe_23
        fake_cpe_data["title"] = "龙龙龙龙"
        test_cpe = CPE(**fake_cpe_data)
        new_fake_cpe_list.append(test_cpe)

        self.session.add_all(new_fake_cpe_list)
        self.session.commit()

    def tearDown(self):
        """
        Remove the test database
        """
        self.session.close()

    def test_check_cpe(self):
        with mock.patch('api.cpe_api.api_functions.get_engine', return_value=self.engine):
            result = api_functions.check_cpe("cpe:/o:hp:j6u57a_firmware:001.1937d")
            assert result

            result = api_functions.check_cpe("some thing that does not exist")
            assert not result

            result = api_functions.check_cpe("a")
            assert not result

    def test_get_common_products(self):
        with mock.patch('api.cpe_api.api_functions.get_engine', return_value=self.engine) as m:
            result = api_functions.get_common_products("hp1", "hp")
            assert len(result) == 0

            result = api_functions.get_common_products("hp", "some_other_vendor")
            assert 'j6u57a_firmware' in result
            assert len(result) == 1

    def test_get_mismatched_vendor_names(self):
        with mock.patch('api.cpe_api.api_functions.get_engine', return_value=self.engine) as m:
            result = api_functions.mismatched_vendor_names()
            assert result == [('micro$oft', 'microsoft'), ('hp', 'hp龙')]

    def test_get_top_10_domains(self):
        with mock.patch('api.cpe_api.api_functions.get_engine', return_value=self.engine) as m:
            results = api_functions.get_top_10_domains()
            assert len(results) == 10
            assert results == ['www.0domain.com', 'www.1domain.com', 'www.2domain.com', 'www.3domain.com', 'www.4domain.com', 'www.5domain.com', 'www.6domain.com', 'www.7domain.com', 'www.8domain.com', 'www.9domain.com']

    def test_get_top_100_versions(self):
        with mock.patch('api.cpe_api.api_functions.get_engine', return_value=self.engine) as m:
            result = api_functions.get_top_100_versions()
            assert len(result) == 100
            assert result[0][1] > result[99][1]

    def test_get_foreign_companies(self):
        with mock.patch('api.cpe_api.api_functions.get_engine', return_value=self.engine) as m:
            result = api_functions.get_foreign_companies()
            assert result == 1
