import httpretty
import os
import unittest
import requests_mock
from main import get_earth_api_images

envs = os.environ
httpretty.enable()


class TestEEApi(unittest.TestCase):
    def set_up(self):
        self.field_id = "LTTest1"
        self.date = "01/01/2023"
        self.lat = "7.9900"
        self.lon = "64.9900"
        self.dim = "0.15"

    def test_call_nasa_api(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri=envs.get(envs.get("NASA_EARTH_API_URL")),
            body={})
        res = get_earth_api_images(self.field_id, self.date, self.lat, self.lon, self.dim)
        assert res == "There was an error"

        httpretty.register_uri(
            method=httpretty.GET,
            uri=envs.get(envs.get("NASA_EARTH_API_URL")),
            body={
                20110101: "http://imagetest.url"
            })

        httpretty.register_uri(
            method=httpretty.GET,
            uri=envs.get(envs.get("http://imagetest.url")),
            body={})
        res = get_earth_api_images(self.field_id, self.date, self.lat, self.lon, self.dim)
        assert res == "Connection to S3 successful..."


