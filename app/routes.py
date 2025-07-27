from flask import render_template, jsonify
from app import app, db
from app.shared_state import shared_data, data_lock
import sqlalchemy as sa
from app.models import Song, PlayedHistory
from app.schedule_manager import listening_manager
from datetime import datetime, timezone


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
        .join(PlayedHistory)
        .group_by(Song.artist)
        .order_by(sa.desc("play_count"))
        .limit(5)
    )
    top_artists = db.session.execute(top_artists_query).all()

    # for artist, pic, count in top_artists:
    #     print(f"{artist} ({pic}): {count} plays")


    most_recent_query = (
        sa.select(
            PlayedHistory,
            Song.album_picture
        )
        .join(Song)
        .order_by(PlayedHistory.timestamp.desc())
        .limit(6)
    )
    recent_plays = db.session.execute(most_recent_query).all()
    # for play, pic in recent_plays:
    #     print(f"{play.song.title} by {play.song.artist} @ {play.timestamp} → {pic}")

    top_songs_query = (
        sa.select(
            Song.title,
            Song.artist,
            Song.album_picture,
            sa.func.count(PlayedHistory.id).label("play_count")
        )
        .join(PlayedHistory)
        .group_by(Song.id, Song.album_picture)
        .order_by(sa.desc("play_count"))
        .limit(5)
    )
    top_songs = db.session.execute(top_songs_query).all()
    # for title, artist, pic, count in top_songs:
    #     print(f"{title} by {artist} ({pic}): {count} plays")

    top_albums_query = (
        sa.select(
            Song.album,
            Song.album_picture,
            sa.func.count(PlayedHistory.id).label("play_count")
        )
        .join(PlayedHistory)
        .group_by(Song.album, Song.album_picture)
        .order_by(sa.desc("play_count"))
        .limit(5)
    )
    top_albums = db.session.execute(top_albums_query).all()

    return render_template(
        'index.html',
        top_artists=top_artists,
        recent_plays=recent_plays,
        top_songs=top_songs,
        top_albums=top_albums
    )

@app.route('/callback')
def callback():
    return "Callback"


@app.route('/api/data', methods=['GET'])
def get_data():
    curr_time = datetime.now(timezone.utc)
    difference_ms = (curr_time - listening_manager.recent_ping_time).total_seconds() * 1000

    if not listening_manager.playing:
        difference_ms = 0
    
    data = {
        "album": listening_manager.album,
        "album_release": listening_manager.album_release,
        "album_picture" : listening_manager.album_picture,
        "artist" : listening_manager.artist,
        "title" : listening_manager.title,

        "position" : listening_manager.position + difference_ms,
        "song_length" : listening_manager.song_length,
        "playing" : listening_manager.playing
    }

    return jsonify(data)