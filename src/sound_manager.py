from typing import List

from loguru import logger

from src.audio_buffer import AudioBuffer
from src.audio_source import AudioSource


class SoundManager:

    _sound_manager = None
    audio_sources: List[AudioSource]

    def __init__(self) -> None:
        # load all sounds
        # pass
        self.buffers = {}
        # sound_files = os.listdir(os.path.join('data', 'sounds'))
        # for f in sound_files:
        #     full_path = os.path.join('data', 'sounds', f)
        #     buffer = self.create_buffer(full_path)
        #     self.buffers[f] = buffer
        self.audio_sources = []

    @staticmethod
    def get_instance():
        if SoundManager._sound_manager is None:
            SoundManager._sound_manager = SoundManager()
        return SoundManager._sound_manager

    def play(self, source: AudioSource, buffer: AudioBuffer, x: int, y: int, loop: bool):
        #source.is_playing = True  # for testing purpose
        logger.info(f"Playing {buffer} at {x}, {y} with loop {loop}")  # for testing purpose

    def get_buffer(self, file_name: str) -> AudioBuffer:
        return file_name  # for testing purpose

    def is_playing(self, source: AudioSource) -> bool:
        return source.is_playing  # for testing purpose

    def stop(self, source: AudioSource) -> None:
        source.is_playing = False  # for testing purpose
        # logger.info("stop()")  # for testing purpose

    def set_source_pos(self, source: AudioSource, x: int, y: int) -> None:
        if source == 'self.source_projectiles_by_id[projectile_id]':
            logger.info(f"{source} set_source_pos({x}, {y})")  # for testing purpose
        pass

    def render_sound(self) -> bytes:
        return bytes(8192)  # for testing purpose

    def create_buffer(self, sound_file: str) -> AudioBuffer:
        return None
    
    def create_source(self) -> AudioSource:
        # logger.info('create a new audio source')
        source = AudioSource(0)
        self.audio_sources.append(source)
        return source
    
    def remove_source(self, source: AudioSource):
        logger.info('free an audio source')
        self.audio_sources.remove(source)

    def stop_all(self):
        logger.info('stop all audio sources')
        for s in self.audio_sources:
            self.stop(s)