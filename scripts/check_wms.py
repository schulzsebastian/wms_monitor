# !usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import requests
import json

def check_wms(url):
    params = {
        'service': 'wms',
        'request': 'getcapabilities'
    }
    r = requests.get(url, params=params, timeout=10)
    r.encoding = 'utf-8'
    if 'WMS_Capabilities' in r.text:
        return True
    return False


if __name__ == '__main__':
    while True:
        check_wms('http://mapy.geoportal.gov.pl/wss/service/img/guest/Administracyjna/MapServer/WMSServer')
        sleep(5)