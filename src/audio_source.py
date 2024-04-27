class AudioSource:
    source_ids = []
    is_playing: bool = False

    def __init__(self, source_ids) -> None:
        self.source_ids = source_ids
    
    def get_source_ids(self):
        return self.source_ids
    
    def close():
        pass
