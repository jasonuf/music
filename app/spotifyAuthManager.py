from dotenv import load_dotenv
import os
import time
import requests
import base64

class SpotifyAuthManager:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
        self.access_token = None
        self.token_expiry_time = 0

    def get_access_token(self):

        if time.time() > self.token_expiry_time - 60:
            self._refresh_access_token()
        
        return self.access_token

    def _refresh_access_token(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        token_data = response.json()

        print(token_data)