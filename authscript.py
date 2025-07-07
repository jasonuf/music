from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

load_dotenv()

client_id_ = os.getenv('CLIENT_ID')
client_secret_ = os.getenv('CLIENT_SECRET')

scope = "user-read-currently-playing user-read-playback-state user-top-read user-read-recently-played"

# Set up the authentication manager
auth_manager = SpotifyOAuth(
    client_id=client_id_,
    client_secret=client_secret_,
    redirect_uri="http://127.0.0.1:5000/",
    scope=scope,
    open_browser=True  # This will automatically open the auth page
)

# This initiates the authentication flow
# The token info (including the refresh token) is stored in the cache
sp = spotipy.Spotify(auth_manager=auth_manager)
recently_played = sp.current_user_recently_played(limit=15)

for dic in recently_played["items"]:
    del dic["track"]["album"]["available_markets"]
    del dic["track"]["available_markets"]


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(recently_played, f, indent=2)   # pretty-print with an indent of 2 spaces

