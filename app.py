# !usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from celery import Celery, task, current_app
from celery.bin import worker
from multiprocessing import Process

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route("/")
def index():
    return render_template("index.html")

@task()
def print_in_flask():
    return print_in_flask.apply_async(countdown=5)

def run_celery(celery):
    w = worker.worker(app=celery)
    p = Process(target=w)
    p.start()
    return celery, p

def run_tasks():
    print_in_flask.apply_async(countdown=5)

def clear_celery(celery, celery_process):
    celery_process.join()
    celery.control.purge()

if __name__ == "__main__":
    celery_process = run_celery(celery)
    run_tasks()
    app.run(debug=True, use_reloader=False)
    clear_celery(*celery_process)
