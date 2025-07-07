from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json



def printMessage(message):
    print("Message: ", message)
    return