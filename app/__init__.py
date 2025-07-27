# app/__init__.py

from flask import Flask
import os
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(20).hex()

redis_url = os.environ.get('REDIS_URL')
if redis_url:
    url = urlparse(redis_url)
    app.config['SCHEDULER_JOBSTORES'] = {
        'default': {
            'type': 'redis',
            'host': url.hostname,
            'port': url.port,
            'password': url.password,
            'db': 0 
        }
    }
else:
    app.config['SCHEDULER_JOBSTORES'] = {
        'default': {'type': 'memory'}
    }
app.config['SCHEDULER_API_ENABLED'] = True

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, schedule_manager





