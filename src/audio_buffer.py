class AudioBuffer:
    buffers = []

    def __init__(self, buffers) -> None:
        self.buffers = buffers

    def get_buffers(self):
        return self.buffers