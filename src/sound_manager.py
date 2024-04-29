import wave
from array import array
from pathlib import Path
from typing import Dict, List

from loguru import logger

from openal import al
from src.audio_buffer import AudioBuffer
from src.audio_source import AudioSource
from src.config import ENABLE_AUDIO_OUTPUT, ENABLE_VIRTUAL_AUDIO
from src.sound_renderer import SoundRenderer

formatmap = {
    (1, 8) : al.AL_FORMAT_MONO8,
    (2, 8) : al.AL_FORMAT_STEREO8,
    (1, 16): al.AL_FORMAT_MONO16,
    (2, 16) : al.AL_FORMAT_STEREO16,
}


class SoundManager:
    _instance = None

    sound_renderers: List[SoundRenderer] = []
    audio_sources: List[AudioSource] = []
    audio_buffers: List[AudioBuffer] = []
    sound_buffers: Dict[str, AudioBuffer] = {}
    virtual_renderer: SoundRenderer = None

    def __init__(self) -> None:
        if ENABLE_AUDIO_OUTPUT:
            self.sound_renderers.append(SoundRenderer.create_default_renderer())
        if ENABLE_VIRTUAL_AUDIO:
            self.virtual_renderer = SoundRenderer.create_virtual_renderer()
            self.sound_renderers.append(self.virtual_renderer)
        if len(self.sound_renderers) == 0:
            raise ValueError("No audio renderer has been created.")
        data_path = Path('data/sounds')
        for file in data_path.iterdir():
            self.sound_buffers[file.name] = self.create_buffer(file)
        logger.info("Sound effects have been loaded.")
        self.set_listener_values()

    def set_listener_values(self) -> None:
        listener_pos = [350.0, 0.0, 0.0]
        listener_vel = [0.0, 0.0, 0.0]
        listener_ori = [0.0, 0.0, -1.0, 0.0, 1.0, 0.0]
        for sound_renderer in self.sound_renderers:
            sound_renderer.al_listener_fv(al.AL_POSITION, listener_pos)
            sound_renderer.al_listener_fv(al.AL_VELOCITY, listener_vel)
            sound_renderer.al_listener_fv(al.AL_ORIENTATION, listener_ori)

    @staticmethod
    def get_instance():
        if SoundManager._instance is None:
            SoundManager._instance = SoundManager()
        return SoundManager._instance

    def play(self, source: AudioSource, buffer: AudioBuffer, x: int, y: int, loop: bool) -> None:
        for i, sound_renderer in enumerate(self.sound_renderers):
            source_id = source.get_source_ids()[i]
            buffer_id = buffer.get_buffers()[i]
            sound_renderer.play(source_id, buffer_id, x, y, loop)

    def get_sound_buffer(self, sound_name: str) -> AudioBuffer:
        return self.sound_buffers.get(sound_name)

    def is_playing(self, source: AudioSource) -> bool:
        ans = False
        for i, sound_renderer in enumerate(self.sound_renderers):
            source_id = source.get_source_ids()[i]
            ans = ans or sound_renderer.is_playing(source_id)
        return ans

    def stop(self, source: AudioSource) -> None:
        for i, sound_renderer in enumerate(self.sound_renderers):
            source_id = source.get_source_ids()[i]
            sound_renderer.stop(source_id)

    def set_source_pos(self, source: AudioSource, x: int, y: int) -> None:
        for i, sound_renderer in enumerate(self.sound_renderers):
            source_id = source.get_source_ids()[i]
            sound_renderer.set_source_3f(source_id, al.AL_POSITION, x, 0, 4)

    def set_source_gain(self, source: AudioSource, gain: float) -> None:
        for i, sound_renderer in enumerate(self.sound_renderers):
            source_id = source.get_source_ids()[i]
            sound_renderer.set_source_gain(source_id, min(1.0, max(0.0, gain)))

    def create_buffer(self, file_path: Path) -> AudioBuffer:
        buffer_ids = [0] * len(self.sound_renderers)
        for i, sound_renderer in enumerate(self.sound_renderers):
            sound_renderer.set()
            buffer_ids[i] = self.register_sound(file_path)
        audio_buffer = AudioBuffer(buffer_ids)
        self.audio_buffers.append(audio_buffer)
        return audio_buffer
        
    def register_sound(self, file_path: Path) -> int:
        buffer = al.ALuint(0)
        al.alGenBuffers(1, buffer)
        wavefp = wave.open(str(file_path), 'rb')
        channels = wavefp.getnchannels()
        bitrate = wavefp.getsampwidth() * 8
        samplerate = wavefp.getframerate()
        wavbuf = wavefp.readframes(wavefp.getnframes())
        alformat = formatmap[(channels, bitrate)]
        al.alBufferData(buffer, alformat, wavbuf, len(wavbuf), samplerate)
        wavefp.close()
        return buffer.value
    
    def create_audio_source(self) -> AudioSource:
        source_ids = [0] * len(self.sound_renderers)
        for i, sound_renderer in enumerate(self.sound_renderers):
            sound_renderer.set()
            source_ids[i] = self.create_source()
        audio_source = AudioSource(source_ids)
        self.audio_sources.append(audio_source)
        return audio_source
    
    def create_source(self) -> int:
        source = al.ALuint(0)
        al.alGenSources(1, source)
        al.alSourcef(source, al.AL_ROLLOFF_FACTOR, 0.01)
        return source.value

    def render_sound(self) -> bytes:
        audio_sample = self.virtual_renderer.sample_audio()
        float_array = array('f', audio_sample.flatten())
        byte_data = float_array.tobytes()
        return byte_data
    
    def remove_source(self, source: AudioSource) -> None:
        for i, sound_renderer in enumerate(self.sound_renderers):
            source_id = source.get_source_ids()[i]
            sound_renderer.delete_source(source_id)
        self.audio_sources.remove(source)

    def stop_all(self) -> None:
        for audio_source in self.audio_sources:
            self.stop(audio_source)

    def close(self) -> None:
        for i, sound_renderer in enumerate(self.sound_renderers):
            for audio_buffer in self.audio_buffers:
                sound_renderer.delete_buffer(audio_buffer.get_buffers()[i])
            for audio_source in self.audio_sources:
                sound_renderer.delete_source(audio_source.get_source_ids()[i])
            sound_renderer.close()
