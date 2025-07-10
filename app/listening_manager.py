class ListeningManager:
    def __init__(self):
        self.current_song = None

    def set_current_song(self, artist, title):
        self.current_song = (artist, title)

    def check_and_update_song(self, artist, title) -> tuple[str, str]:
        if (artist, title) == self.current_song:
            return None
        else:
            temp = self.current_song
            self.current_song = (artist, title)
            return temp
