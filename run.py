# !usr/bin/python
# -*- coding: utf-8 -*-
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop
from app import app

if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'.*', FallbackHandler, dict(fallback=container))
    ], debug=True)
    server.listen(5000)
    main_loop = IOLoop.instance()
    main_loop.start()
