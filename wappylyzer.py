# -*- coding: utf-8 -*-

import re
import json
import requests
from bs4 import BeautifulSoup


WAPPALYZER_APPS_URL = 'https://raw.githubusercontent.com/AliasIO/Wappalyzer/master/src/apps.json'


def as_list(value):
    if isinstance(value, list):
        return value

    return [value]


def is_html_document(html):
    return bool(html.find('html'))


class Wappylyzer(object):
    """
    Class that parses the `apps.json` file and analyze an HTTP response.
    """

    @classmethod
    def update(clz, dest_file):
        r = requests.get(WAPPALYZER_APPS_URL)

        with open(dest_file, 'w') as fd:
            fd.write(r.content)

    def __init__(self, apps):
        self.__apps_file = apps
        self.__apps = {}
        self.__categories = {}
        self.parse_apps()

    def parse_apps(self):
        with open(self.__apps_file, 'r') as fd:
            datas = json.loads(fd.read())

        self.__categories = datas.get('categories', {})
        self.__apps = {}
        for app_name, app in datas.get('apps', {}).items():
            self.__apps[app_name] = self.parse_app(app_name, app)

    def request_url(self, url):
        return requests.get(url)

    def parse_app(self, app_name, app):
        app['name'] = app_name
        return app

    def iter_apps(self, key):
        for (app_name, app) in self.__apps.items():
            if key in app:
                patterns = self.parse_patterns(app.get(key))
                yield (app, patterns)

    def parse_patterns(self, patterns):
        if not patterns:
            return []

        parsed = {}

        if type(patterns) in (str, list):
            patterns = {
                'main': as_list(patterns)
            }

        for key, pattern_value in patterns.items():
            parsed[key] = []

            for pattern in as_list(pattern_value):
                attrs = {}
                pattern = pattern.split('\\;')

                for i in range(0, len(pattern)):
                    attr = pattern[i]

                    if i == 0:
                        attrs['string'] = attr

                        try:
                            attrs['regex'] = re.compile(attr, re.I)
                        except re.error:
                            attrs['regex'] = re.compile('', re.I)
                            print('[-] Error with regex %s' % attr)

                    else:
                        attr = attr.split(':')

                        if len(attr) > 1:
                            attrs[attr[0]] = ':'.join(attr[1:])

                parsed[key].append(attrs)

        if 'main' in parsed:
            parsed = parsed['main']

        return parsed

    def add_detected(self, app, pattern, type, value, key=None):
        print(type, '=>', app['name'])

        if 'version' in pattern:
            matches = pattern['regex'].match(value)

            if matches:
                print('  - version', matches.groups())

    def get_scripts(self, html):
        return filter(bool, map(lambda s: s.attrs.get('src'), html.find_all('script')))

    def get_meta_tags(self, html):
        return html.find_all('meta')

    def analyze_from_url(self, url):
        res = self.request_url(url)
        return self.analyze(res)

    def analyze(self, response):
        url = response.url
        html_doc = response.text
        html = BeautifulSoup(html_doc, 'html.parser')

        if is_html_document(html):
            scripts = self.get_scripts(html)
            meta_tags = self.get_meta_tags(html)

            self.analyze_html(html_doc)
            self.analyze_scripts(scripts)
            self.analyze_meta(meta_tags)

        self.analyze_url(url)
        self.analyze_headers(response.headers)
        self.analyze_cookies(response.cookies)

    def analyze_url(self, url):
        for (app, patterns) in self.iter_apps('url'):
            for pattern in patterns:
                if pattern['regex'].search(url):
                    self.add_detected(app, pattern, 'url', url)

    def analyze_html(self, html):
        for (app, patterns) in self.iter_apps('html'):
            for pattern in patterns:
                if pattern['regex'].search(html):
                    self.add_detected(app, pattern, 'html', html)

    def analyze_scripts(self, scripts):
        for (app, patterns) in self.iter_apps('script'):
            for uri in scripts:
                for pattern in patterns:
                    if pattern['regex'].search(uri):
                        self.add_detected(app, pattern, 'script', uri)

    def analyze_cookies(self, cookies):
        for (app, cookies_patterns) in self.iter_apps('cookies'):
            for cookie_name, patterns in cookies_patterns.items():
                if cookie_name in cookies:
                    for pattern in patterns:
                        if pattern['regex'].search(cookies[cookie_name]):
                            self.add_detected(app, pattern, 'cookies', cookies[cookie_name], cookie_name)

    def analyze_headers(self, headers):
        for (app, headers_patterns) in self.iter_apps('headers'):
            for header_name, patterns in headers_patterns.items():
                if header_name in headers:
                    for pattern in patterns:
                        if pattern['regex'].search(headers[header_name]):
                            self.add_detected(app, pattern, 'headers', headers[header_name], header_name)

    def analyze_meta(self, meta_tags):
        for (app, meta_patterns) in self.iter_apps('meta'):
            for meta_tag in meta_tags:
                meta_name = meta_tag.attrs.get('name', '').lower()
                meta_property = meta_tag.attrs.get('property', '').lower()
                meta_content = meta_tag.attrs.get('content')

                if meta_name or meta_property:
                    for meta_pattern_name, patterns in meta_patterns.items():
                        if meta_pattern_name in (meta_name, meta_property):
                            for pattern in patterns:
                                if pattern['regex'].search(meta_content):
                                    self.add_detected(app, pattern, 'meta', meta_content, meta_pattern_name)

    def analyze_js(self, js):
        raise NotImplementedError('Wappylyzer:analyze_js')
