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

        if response.status_code == 200:
            self.token_expiry_time = time.time() + token_data.get("expires_in", 0)
            self.access_token = token_data.get("access_token")
        else:
            print("Error, Response code: ", response.status_code)
    
    def get_recently_played(self, limit=10):
        token = self.get_access_token()

        if token is None:
            print("Error: Token is None")
            return {}

        url = "https://api.spotify.com/v1/me/player/recently-played" + "?limit=" + str(limit)
        headers = {
            "Authorization": "Bearer " + token
        }

        response = requests.get(url=url, headers=headers)
        recently_played_data = response.json()

        #print("GET RECENTLY PLAYED DATA: ", recently_played_data)

        return recently_played_data
    
    def get_playing(self):
        token = self.get_access_token()

        if token is None:
            print("Error: Token is None")
            return {}

        url = "https://api.spotify.com/v1/me/player"
        headers = {
            "Authorization": "Bearer " + token
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code == 200:
            song_info = response.json()
            song_info['status_code'] = 200
            #print("SONG INFO: ", song_info)
            return song_info
        elif response.status_code == 204: #Playback not available or active
            return {'status_code': 204}
        elif response.status_code == 429: #The app has exceeded its rate limits.
            return {'status_code': 429}
        else: #token or oauth failure
            return {'status_code': 100}