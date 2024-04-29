from typing import List


class AudioBuffer:
    buffers: List[int]

    def __init__(self, buffers: List[int]) -> None:
        self.buffers = buffers

    def get_buffers(self) -> List[int]:
        return self.buffers
