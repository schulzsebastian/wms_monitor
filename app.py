# !usr/bin/python
# -*- coding: utf-8 -*-
from tornado.web import RequestHandler

class MainHandler(RequestHandler):
    def get(self):
        self.render("templates/index.html")
