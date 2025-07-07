# app/__init__.py

from flask import Flask
from flask_apscheduler import APScheduler
from .utils import printMessage 
from config import Config

scheduler = APScheduler()
app = Flask(__name__)
app.config.from_object(Config)

scheduler.init_app(app)
scheduler.add_job(
    id='print_hello_world',
    func=printMessage,
    args=('hello from the scheduler!',),
    trigger='interval',
    seconds=3
)
scheduler.start()


from app import routes
