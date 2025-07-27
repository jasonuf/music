from flask_apscheduler import APScheduler
from app import app, db
from app.spotify_auth_manager import SpotifyAuthManager
from app.listening_manager import ListeningManager
from datetime import datetime, timezone, timedelta
from app.models import Song, PlayedHistory
import sqlalchemy as sa



class SchedulerInternal:
    def __init__(self):
        self.no_song_count = 0
    
    def reset_no_song_count(self):
        self.no_song_count = 0
    
    def increment_no_song_count(self):
        self.no_song_count += 1
        
        if self.no_song_count >= 8:
            self.no_song_count = 0
            return True
        else:
            return False



scheduler = APScheduler()
scheduler.init_app(app)
auth_manager = SpotifyAuthManager()
internal_scheduler = SchedulerInternal()
listening_manager = ListeningManager()


@scheduler.task('interval', id='check_listening_session', seconds=120, misfire_grace_time=50)
def check_listening_session():

    data = auth_manager.get_playing()
    status_code = data['status_code']

    if status_code == 200:
        #switch to other schedule
        print("\nPLAYING DETECTED, SWITCHING TO ACTIVE POLLING\n")
        scheduler.pause_job('check_listening_session')
        internal_scheduler.reset_no_song_count()
        scheduler.resume_job('playing')
        playing()
    else:
        print("\nNO PLAYING DETECTED\n")

def schedule_end_of_song(progress_ms, duration_ms, track_id):
    remaining_s = (duration_ms - progress_ms) / 1000.0 + 1
    run_time = datetime.now(timezone.utc) + timedelta(seconds=remaining_s)

    job_id = f'playing_end_{track_id}'

    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass

    print("PREFIRE SCHEDULED")
    scheduler.add_job(
        func=playing,
        trigger='date',
        run_date=run_time,
        id=job_id,
        misfire_grace_time=5
    )

PLAYING_INTERVAL = 25
@scheduler.task('interval', id='playing', seconds=PLAYING_INTERVAL, misfire_grace_time=7)
def playing():
    ''' 
    NEEDED DATA TO UPDATE DATABASE:

    title
    artist
    album
    album release date
    album picture

    timestamp  
    '''

    data = auth_manager.get_playing()
    status_code = data['status_code']

    print()
    print("TASK - PLAYING, RESPONSE WITH CODE: ", status_code)
    print()

    if status_code == 204:
        if internal_scheduler.increment_no_song_count():
            print()
            print("PLAYING STOPPED - SWITCHING TO CHECK_LISTENING_SESSION")
            print()
            scheduler.pause_job('playing')
            internal_scheduler.reset_no_song_count()
            listening_manager.current_song = None
            scheduler.resume_job('check_listening_session')
        return
    
    elif status_code == 200:

        internal_scheduler.reset_no_song_count()

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
            progress_ms = data['progress_ms']
            duration_ms = data['item']['duration_ms']
            is_playing = data['is_playing']

            print()
            print("TRACK: ", title)
            print("ALBUM: ", album)
            print("ALBUM_RELEASE_DATE: ", album_release_date)
            print("ALBUM_PICTURE: ", album_picture)
            print("ARTIST: ", artist)
            print("TIMESTAMP: ", timestamp)
            print()

            new_song = listening_manager.check_and_update_song(artist=artist, title=title)
            listening_manager.set_state(album=album, 
                                        album_release=album_release_date, 
                                        album_picture=album_picture,
                                        artist=artist,
                                        title=title,
                                        progress_ms=progress_ms,
                                        duration_ms=duration_ms,
                                        playing=is_playing)

            if (duration_ms - progress_ms) / 1000.0 <= PLAYING_INTERVAL:
                schedule_end_of_song(progress_ms, duration_ms, title)


            if new_song:
                print()
                print("NEW SONG DETECTED, ADDING TO DB")
                print()
                song_query = sa.select(Song).filter_by(title=title, artist=artist)
                song = db.session.execute(song_query).scalar_one_or_none()

                if song is None:
                    song = Song(title=title, artist=artist, album=album, album_picture=album_picture, album_release_date=album_release_date)
                    db.session.add(song)

                new_play = PlayedHistory(song=song)
                db.session.add(new_play)

                db.session.commit()

scheduler.pause_job('playing')

scheduler.start()