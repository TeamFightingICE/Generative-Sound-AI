from loguru import logger

from src.audio_buffer import AudioBuffer
from src.audio_source import AudioSource


class SoundManager:
    def __init__(self) -> None:
        pass

    def play(self, source: AudioSource, buffer: AudioBuffer, x: int, y: int, loop: bool):
        logger.info(f"Playing {buffer} at {x}, {y} with loop {loop}")

    def get_buffer(self, file_name: str) -> AudioBuffer:
        return file_name  # for testing purpose

    def is_playing(self, source: AudioSource) -> bool:
        return False  # for testing purpose

    def stop(self, source: AudioSource) -> None:
        pass

    def set_source_pos(self, source: AudioSource, x: int, y: int) -> None:
        pass

    def render_sound(self) -> bytes:
        return bytes(8192)  # for testing purpose
