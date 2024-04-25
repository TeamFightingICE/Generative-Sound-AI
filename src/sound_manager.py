from loguru import logger

from src.audio_buffer import AudioBuffer
from src.audio_source import AudioSource

import openal
import os

class SoundManager:

    _sound_manager = None

    def __init__(self) -> None:
        # load all sounds
        # pass
        self.buffers = {}
        sound_files = os.listdir(os.path.join('data', 'sounds'))
        for f in sound_files:
            full_path = os.path.join('data', 'sounds', f)
            buffer = self.create_buffer(full_path)
            self.buffers[f] = buffer
            
    @staticmethod
    def get_instance():
        if SoundManager._sound_manager is None:
            SoundManager._sound_manager = SoundManager()
            return SoundManager._sound_manager

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

    def create_buffer(self, sound_file: str) -> AudioBuffer:
        return None
    
    def create_source(self) -> AudioSource:
        return None
    