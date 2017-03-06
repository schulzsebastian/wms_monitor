# !usr/bin/python
# -*- coding: utf-8 -*-
from tornado.web import Application
from tornado.ioloop import IOLoop
from multiprocessing import Process
from scripts.check_wms import Geoportal
from app import MainHandler

def start_wms_monitor():
    print("Starting monitor...")
    Geoportal(log=True).enable_monitoring()


if __name__ == "__main__":
    settings = {
        "static_path": "static",
        "debug": True
    }
    server = Application([
        (r"/", MainHandler)
    ], **settings)
    server.listen(5000)
    main_loop = IOLoop.instance()
    monitor = Process(target=start_wms_monitor)
    monitor.start()
    try:
        main_loop.start()
    except KeyboardInterrupt:
        main_loop.stop()
        monitor.terminate()
