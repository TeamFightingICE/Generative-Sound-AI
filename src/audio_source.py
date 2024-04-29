class AudioSource:
    source_ids = []

    def __init__(self, source_ids) -> None:
        self.source_ids = source_ids
    
    def get_source_ids(self):
        return self.source_ids
