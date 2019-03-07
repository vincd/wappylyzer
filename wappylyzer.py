# -*- coding: utf-8 -*-

import requests


WAPPALYZER_APPS_URL = 'https://raw.githubusercontent.com/AliasIO/Wappalyzer/master/src/apps.json'


class Wappylyzer(object):
    """
    Class that parse the `apps.json` file and analyze an HTTP response.
    """

    @classmethod
    def update(clz, dest_file):
        r = requests.get(WAPPALYZER_APPS_URL)

        with open(dest_file, 'w') as fd:
            fd.write(r.content)

    def __init__(self, apps):
        self.__apps = {}

    def request_url(self, url):
        return requests.get(url)

    def analyze_url(self, url):
        res = self.request_url(url)
        return self.analyze_response(res)

    def analyze_response(self, response):
        print response
