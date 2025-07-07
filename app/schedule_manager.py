from flask_apscheduler import APScheduler
from app import app
from app.shared_state import shared_data, data_lock
from app.spotify_auth_manager import SpotifyAuthManager

scheduler = APScheduler()
scheduler.init_app(app)
auth_manager = SpotifyAuthManager()

@scheduler.task('interval', id='recently_played', seconds=60, misfire_grace_time=500)
def recently_played():
    
    recently_played = auth_manager.get_recently_played(limit=10)

    artist_song = []

    for dic in recently_played["items"]:
        artists = dic["track"]["artists"]
        artist = ""
        if artists:
            artist = artists[0]["name"]
        name = dic["track"]["name"]
        artist_song.append((artist, name))

    with data_lock:
        shared_data["recently_played"] = artist_song

scheduler.start()