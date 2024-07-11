import urllib

import requests
from unittest import TestCase
from fastapi.testclient import TestClient
from root import app

SERVER_ROOT = "http://127.0.0.1:8000"


class TestRoot(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_cpe(self):
        test_url = urllib.parse.urljoin(SERVER_ROOT, "get_cpe")
        result = self.client.get(test_url, params={"cpe_string": "no find this"})
        assert result.text == "false"

        result = self.client.get(test_url, params={"cpe_string": "cpe:/a:istio:istio:1.2.2"})
        assert result.text == "true"


    def test_get_common_products(self):
        test_url = urllib.parse.urljoin(SERVER_ROOT, "get_common_products")
        result = self.client.get(test_url, params={"vendor1": "znc", "vendor2": "znc"})
        out_list = eval(result.text) # TODO: This is terrible, fix it
        assert out_list == ["znc_docker_image", "znc", "znc-msvc"]

