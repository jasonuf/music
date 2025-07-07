# app/__init__.py

from flask import Flask
from flask_apscheduler import APScheduler
from config import Config
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(20).hex()


from app import routes, schedule_manager





