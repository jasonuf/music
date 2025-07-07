from dotenv import load_dotenv
import os
import time
import requests
import base64
import json

class SpotifyAuthManager:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.refresh_token = os.getenv("REFRESH_TOKEN")
        print(self.client_id)
        print(self.client_secret)
        print(self.refresh_token)
        self.access_token = None
        self.token_expiry_time = 0

        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError(
                "Spotify credentials are missing. Ensure SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and REFRESH_TOKEN are set."
            )

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
        print("RESPONSE: ", response, " RESPONSE CODE: ", response.status_code, " TOKEN DATA: ", token_data)

        self.token_expiry_time = time.time() + token_data.get("expires_in", 0)
        self.access_token = token_data.get("access_token")
    
    def get_recently_played(self, limit=10):
        token = self.get_access_token()

        url = "https://api.spotify.com/v1/me/player/recently-played" + "?limit=" + str(limit)
        headers = {
            "Authorization": "Bearer " + token
        }

        response = requests.get(url=url, headers=headers)
        recently_played_data = response.json()

        print("RESPONSE TYPE: ", type(recently_played_data))
        print("GET RECENTLY PLAYED DATA: ", recently_played_data)
        return recently_played_data
