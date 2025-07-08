from flask import render_template
from app import app, db
from app.shared_state import shared_data, data_lock
import sqlalchemy as sa
from app.models import Song, PlayedHistory

@app.route('/')
@app.route('/index')
def index():

    '''
    Global variable for testing:
    with data_lock:
        result = shared_data.get("recently_played", [])
    '''
    
    top_artists_query = (
        sa.select(
            Song.artist,
            sa.func.count(PlayedHistory.id).label("play_count")
        )
        .join(Song)
        .group_by(Song.artist)
        .order_by(sa.desc("play_count"))
        .limit(5)
    )
    top_artists = db.session.execute(top_artists_query).all()
    # for artist, count in top_artists:
    #     print(f"{artist}: {count} plays")

    most_recent_query = (
        sa.select(PlayedHistory)
        .order_by(PlayedHistory.timestamp.desc())
        .limit(10)
    )
    recent_plays = db.session.execute(most_recent_query).scalars().all()
    # for play in recent_plays:
    #     print(f"'{play.song.title}' by {play.song.artist} played at {play.timestamp}")

    top_songs_query = (
        sa.select(
            Song.title,
            Song.artist,
            sa.func.count(PlayedHistory.id).label("play_count")
        )
        .join(PlayedHistory)
        .group_by(Song.id)
        .order_by(sa.desc("play_count"))
        .limit(10)
    )
    top_songs = db.session.execute(top_songs_query).all()
    # for title, artist, count in top_songs:
    #     print(f"'{title}' by {artist}: {count} plays")

        
    return render_template('index.html', top_artists=top_artists, recent_plays=recent_plays, top_songs=top_songs)

@app.route('/callback')
def callback():
    return "Callback"