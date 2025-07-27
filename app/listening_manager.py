from datetime import datetime, timezone


class ListeningManager:
    def __init__(self):
        self.current_song = None
        
        self.album = None
        self.album_release = None
        self.album_picture = None
        self.artist = None
        self.title = None

        self.position = 0
        self.song_length = 0
        self.playing = False
        self.recent_ping_time = datetime.now(timezone.utc)
    
    def set_state(self, album, album_release, album_picture, artist, title, progress_ms, duration_ms, playing):
        self.album = album
        self.album_release = album_release
        self.album_picture = album_picture
        self.artist = artist
        self.title = title

        self.position = progress_ms
        self.song_length = duration_ms
        self.playing = playing
        self.recent_ping_time = datetime.now(timezone.utc)


    def set_current_song(self, artist, title):
        self.current_song = (artist, title)

    def check_and_update_song(self, artist, title) -> tuple[str, str]:
        if (artist, title) == self.current_song:
            return False
        else:
            self.current_song = (artist, title)
            return True

    

    