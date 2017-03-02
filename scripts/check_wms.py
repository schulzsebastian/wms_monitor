# !usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import sleep, strftime
import requests


class Geoportal(object):
    def __init__(self, log=False):
        self.log = log
        self.url = "http://www.geoportal.gov.pl/uslugi/usluga-przegladania-wms"

    def url_list(self):
        urls = []
        r = requests.get("http://www.geoportal.gov.pl/uslugi/usluga-przegladania-wms")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for row in soup.find_all("td"):
                urls.append({
                    "name": row.find_all("p")[0].string,
                    "url": row.find_all("p")[1].string
                })
        return urls

    def check_url(self, url):
        params = {
            "service": "wms",
            "request": "getcapabilities"
        }
        error = ""
        try:
            r = requests.get(url, params=params, timeout=20)
            if r.status_code == 200:
                r.encoding = "utf-8"
                if "WMS_Capabilities" in r.text:
                    return ""
                else:
                    error = "[{}] Invalid content ({})".format(strftime("%c"), url)
            else:
                error = "[{}] Invalid status code ({})".format(strftime("%c"), url)
        except requests.exceptions.ReadTimeout:
            error = "[{}] Time out ({})".format(strftime("%c"), url)
        if self.log:
            print(error)
        return error

    def check_urls(self):
        return not bool(self.invalid_wms_list())

    def invalid_wms_list(self):
        return [u for u in self.url_list() if self.check_url(u["url"])]

if __name__ == "__main__":
    wms = Geoportal(log=True)
    while True:
        wms.check_urls()
