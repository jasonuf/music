# app/__init__.py

from flask import Flask
from flask_apscheduler import APScheduler
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(20).hex()

redis_url = os.environ.get('REDIS_URL')

if redis_url:
    # If on Railway with Redis, parse the URL and configure the job store
    url = urlparse(redis_url)
    app.config['SCHEDULER_JOBSTORES'] = {
        'default': {
            'type': 'redis',
            'host': url.hostname,
            'port': url.port,
            'password': url.password,
            'db': 0  # Use the default Redis database
        }
    }
else:
    # For local development without Redis, use the default in-memory store
    app.config['SCHEDULER_JOBSTORES'] = {
        'default': {'type': 'memory'}
    }
app.config['SCHEDULER_API_ENABLED'] = True

from app import routes, schedule_manager





