from spotify_auth_manager import SpotifyAuthManager
from app import db
import sqlalchemy as sa
from models import Song, PlayedHistory

# manager = SpotifyAuthManager()

# playing = manager.get_playing()

all_songs = db.session.execute(sa.select(Song)).scalars().all()
for item in all_songs:
    print(item)