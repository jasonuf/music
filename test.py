from app.spotify_auth_manager import SpotifyAuthManager
from app import app, db
import sqlalchemy as sa
from app.models import Song, PlayedHistory

# manager = SpotifyAuthManager()

# playing = manager.get_playing()

with app.app_context():
    all_songs = db.session.execute(sa.select(Song)).scalars().all()
    for item in all_songs:
        print(item)