# app/__init__.py

from flask import Flask
from flask_apscheduler import APScheduler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes, schedule_manager





