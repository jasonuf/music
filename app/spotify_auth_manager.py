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
        self.refresh_token = os.getenv("REFRESH_TOKEN")
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
            "refresh_token": self.refresh_token,
        }

        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        token_data = response.json()
        print("TOKEN DATA: ", token_data)

        self.access_token = token_data["access_token"]
    
    def get_recently_played(self):
        token = self.get_access_token()

        url = "https://api.spotify.com/v1/me/player/recently-played"
        header = {
            "Authorization": "Bearer " + token
        }

        response = requests.get(url=url, header=header)
        print(response)
