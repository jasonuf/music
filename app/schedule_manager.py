from flask_apscheduler import APScheduler
from app import app
from app.shared_state import shared_data, data_lock
from app.spotify_auth_manager import SpotifyAuthManager

import time


scheduler = APScheduler()
scheduler.init_app(app)

@scheduler.task('interval', id='do_job_1', seconds=60, misfire_grace_time=10)
def job1():
    auth_manager = SpotifyAuthManager
    
    with data_lock:
        shared_data["value"] = "Temp Value"

scheduler.start()