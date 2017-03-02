# !usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import sleep
import requests
import json

def check_wms(url):
    params = {
        'service': 'wms',
        'request': 'getcapabilities'
    }
    r = requests.get(url, params=params, timeout=10)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        if 'WMS_Capabilities' in r.text:
            return True
    return False


def parse_geoportal():
    urls = []
    r = requests.get('http://www.geoportal.gov.pl/uslugi/usluga-przegladania-wms')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        for row in soup.find_all('td'):
            urls.append(row.find_all('p')[1].string)
    return urls


if __name__ == '__main__':
    while True:
        for url in parse_geoportal():
            print(check_wms(url))
            sleep(1)
