from typing import List


class AudioSource:
    source_ids: List[int]

    def __init__(self, source_ids: List[int]) -> None:
        self.source_ids = source_ids
    
    def get_source_ids(self) -> List[int]:
        return self.source_ids
