import ctypes
from typing import List

import numpy as np

from openal import al, alc
from src.config import (ALC_FLOAT_SOFT, ALC_FORMAT_CHANNELS_SOFT,
                        ALC_FORMAT_TYPE_SOFT, ALC_FREQUENCY, ALC_STEREO_SOFT,
                        SAMPLE_SIZE, SOUND_SAMPLING_RATE)


class SoundRenderer:
    device = None
    context = None

    def __init__(self, device, context) -> None:
        self.device = device
        self.context = context

    @staticmethod
    def create_default_renderer():
        device = alc.alcOpenDevice(None)
        context = alc.alcCreateContext(device, None)
        alc.alcMakeContextCurrent(context)
        return SoundRenderer(device, context)

    @staticmethod
    def create_virtual_renderer():
        device = alc.alcLoopbackOpenDeviceSOFT(None)
        attrs = [ALC_FORMAT_TYPE_SOFT, ALC_FLOAT_SOFT, ALC_FORMAT_CHANNELS_SOFT,
                 ALC_STEREO_SOFT, ALC_FREQUENCY, SOUND_SAMPLING_RATE, 0]
        attrs_c = alc.ALCint * len(attrs)
        attrs_c = attrs_c(*attrs)
        context = alc.alcCreateContext(device, attrs_c)
        return SoundRenderer(device, context)

    def set(self) -> None:
        alc.alcMakeContextCurrent(self.context)

    def set_listener_data(self) -> None:
        self.set()
        al.alListener3f(al.AL_POSITION, 0, 0, 0)
        al.alListener3f(al.AL_VELOCITY, 0, 0, 0)

    def play(self, source_id: int, buffer_id: int) -> None:
        self.set()
        al.alSourcei(source_id, al.AL_BUFFER, buffer_id)
        al.alSourcePlay(source_id)

    def stop(self, source_id: int) -> None:
        self.set()
        if self.is_playing(source_id):
            al.alSourceStop(source_id)

    def play(self, source_id: int, buffer_id: int, x: int, y: int, loop: bool) -> None:
        self.set()
        if self.is_playing(source_id):
            self.stop(source_id)
        al.alSourcei(source_id, al.AL_BUFFER, buffer_id)
        al.alSource3f(source_id, al.AL_POSITION, x, 0, 4)
        al.alSourcei(source_id, al.AL_LOOPING, int(loop))
        al.alSourcePlay(source_id)

    def get_source_gain(self, source_id: int) -> float:
        self.set()
        return al.alGetSourcef(source_id, al.AL_GAIN)

    def set_source_gain(self, source_id: int, gain: float) -> None:
        self.set()
        al.alSourcef(source_id, al.AL_GAIN, gain)

    def set_source_3f(self, source_id: int, param: int, x: int, y: int, z: int) -> None:
        self.set()
        al.alSource3f(source_id, param, x, y, z)

    def delete_source(self, source_id: int) -> None:
        self.set()
        al.alDeleteSources(1, alc.ALCuint(source_id))

    def delete_buffer(self, buffer_id: int) -> None:
        self.set()
        al.alDeleteBuffers(1, alc.ALCuint(buffer_id))

    def close(self) -> None:
        self.set()
        alc.alcDestroyContext(self.context)
        alc.alcCloseDevice(self.device)

    def is_playing(self, source_id: int) -> bool:
        self.set()
        state = alc.ALCint(0)
        al.alGetSourcei(source_id, al.AL_SOURCE_STATE, state)
        return state.value == al.AL_PLAYING

    def al_listener_fv(self, param: int, values: List[float]) -> None:
        self.set()
        values_arr = (alc.ALCfloat * len(values))(*values)
        al.alListenerfv(param, values_arr)

    def sample_audio(self) -> np.ndarray[np.float32]:
        self.set()
        audio_data_type = alc.ALCfloat * SAMPLE_SIZE * 2
        audio_sample = audio_data_type()
        audio_sample_pointer = ctypes.cast(audio_sample, ctypes.c_void_p)

        alc.alcRenderSamplesSOFT(self.device, audio_sample_pointer, al.ALsizei(SAMPLE_SIZE))
        sampled_audio = ctypes.cast(audio_sample_pointer, ctypes.POINTER(audio_data_type)).contents

        separated_channel_audio = np.zeros((2, 1024), dtype=np.float32)
        separated_channel_audio[0, :SAMPLE_SIZE] = sampled_audio[0]
        separated_channel_audio[1, :SAMPLE_SIZE] = sampled_audio[1]
        return separated_channel_audio
