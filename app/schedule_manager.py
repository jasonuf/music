from flask_apscheduler import APScheduler
from app import app, db
from app.shared_state import shared_data, data_lock
from app.spotify_auth_manager import SpotifyAuthManager
from datetime import datetime, timezone
from app.models import Song, PlayedHistory
import sqlalchemy as sa

scheduler = APScheduler()
scheduler.init_app(app)
auth_manager = SpotifyAuthManager()

'''
@scheduler.task('interval', id='recently_played', seconds=2700, misfire_grace_time=500)
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
'''

@scheduler.task('interval', id='playing', seconds=100, misfire_grace_time=50)
def playing():
    data = auth_manager.get_playing()
    ''' 
    NEEDED DATA TO UPDATE DATABASE:

    title
    artist
    album
    album release date
    album picture

    timestamp  
    '''
    status_code = data['status_code']
    print("TASK - PLAYING, RESPONSE WITH CODE: ", status_code)

    if status_code == 204:
        #no content
        return
    elif status_code == 200:
        with app.app_context():
            trackDict = data['item']
            album = trackDict['album']['name']
            album_release_date = trackDict['album']['release_date']
            album_picture = None
            if trackDict['album']['images']:
                album_picture = trackDict['album']['images'][0]['url']
            artist = trackDict['artists'][0]['name']
            title = trackDict['name']
            timestamp = datetime.fromtimestamp(data['timestamp']/1000.0, tz=timezone.utc)

            print("TRACK: ", title)
            print("ALBUM: ", album)
            print("ALBUM_RELEASE_DATE: ", album_release_date)
            print("ALBUM_PICTURE: ", album_picture)
            print("ARTIST: ", artist)
            print("TIMESTAMP: ", timestamp)

            song_query = sa.select(Song).filter_by(title=title, artist=artist)
            song = db.session.execute(song_query).scalar_one_or_none()

            if song is None:
                song = Song(title=title, artist=artist, album=album, album_picture=album_picture, album_release_date=album_release_date)
                db.session.add(song)

            new_play = PlayedHistory(song=song)
            db.session.add(new_play)

            db.session.commit()


scheduler.start()