# app/__init__.py

from flask import Flask
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(20).hex()

app.config['SCHEDULER_JOBSTORES'] = {
    'default': {
        'type': 'redis',
        'url': os.environ.get('REDIS_URL')
    }
}
app.config['SCHEDULER_API_ENABLED'] = True

from app import routes, schedule_manager





