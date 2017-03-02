# !usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import sleep
import requests


class Geoportal(object):
    def __init__(self):
        self.url = 'http://www.geoportal.gov.pl/uslugi/usluga-przegladania-wms'

    def url_list(self):
        urls = []
        r = requests.get('http://www.geoportal.gov.pl/uslugi/usluga-przegladania-wms')
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for row in soup.find_all('td'):
                urls.append(row.find_all('p')[1].string)
        return urls

    def check_url(self, url):
        params = {
            'service': 'wms',
            'request': 'getcapabilities'
        }
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            if 'WMS_Capabilities' in r.text:
                return True
        return False

    def check_urls(self):
        return not bool(self.invalid_urls())

    def invalid_urls(self):
        return [url for url in self.url_list() if not self.check_url(url)]

if __name__ == '__main__':
    while True:
        wms = Geoportal()
        print(wms.check_urls())
        print(wms.invalid_urls())
        sleep(5)
