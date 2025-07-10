class ListeningManager:
    def __init__(self):
        self.current_song = None

    def set_current_song(self, artist, title):
        self.current_song = (artist, title)

    def check_and_update_song(self, artist, title) -> tuple[str, str]:
        if (artist, title) == self.current_song:
            return False
        else:
            self.current_song = (artist, title)
            return True
