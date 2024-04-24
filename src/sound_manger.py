from audio_source import AudioSource
from audio_buffer import AudioBuffer


class SoundManager:
    def __init__(self) -> None:
        pass

    def play(self, source: AudioSource, buffer: AudioBuffer, x: int, y: int, loop: bool):
        pass

    def get_buffer(self, file_name) -> AudioBuffer:
        pass

    def is_playing(self, source) -> bool:
        pass

    def stop(self, source: AudioSource):
        pass

    def set_source_pos(self, x, y):
        pass

    def render_sound(self):
        pass