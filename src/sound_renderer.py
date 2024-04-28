import ctypes

from openal import al, alc
from typing import List
from src.config import SAMPLE_SIZE

ALC_FORMAT_TYPE_SOFT = 6545
ALC_FLOAT_SOFT = 5126
ALC_FORMAT_CHANNELS_SOFT = 6544
ALC_STEREO_SOFT = 5377
ALC_FREQUENCY = 4103
SOUND_SAMPLING_RATE = 48000


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
        attrs_c = ctypes.c_int * len(attrs)
        attrs_c = attrs_c(*attrs)
        context = alc.alcCreateContext(device, attrs_c)
        return SoundRenderer(device, context)

    def set(self):
        alc.alcMakeContextCurrent(self.context)

    def setListenerData(self):
        self.set()
        al.alListener3f(al.AL_POSITION, 0, 0, 0)
        al.alListener3f(al.AL_VELOCITY, 0, 0, 0)

    def play(self, source_id: int, buffer_id: int) -> None:
        self.set()
        al.alSourcei(source_id, al.AL_BUFFER, buffer_id)
        al.alSourcePlay(source_id)

    def stop(self, source_id: int):
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

    def set_source_3f(self, source_id: int, param, x: int, y: int, z: int) -> None:
        self.set()
        al.alSource3f(source_id, param, x, y, z)

    def delete_source(self, source_id: int) -> None:
        self.set()
        al.alDeleteSources(source_id)

    def delete_buffer(self, buffer_id: int) -> None:
        self.set()
        al.alDeleteBuffers(buffer_id)

    def close(self):
        self.set()
        alc.alcDestroyContext(self.context)
        alc.alcCloseDevice(self.device)

    def is_playing(self, source_id: int) -> bool:
        self.set()
        state = ctypes.c_int(0)
        al.alGetSourcei(source_id, al.AL_SOURCE_STATE, ctypes.byref(state))
        return state.value == al.AL_PLAYING

    def al_listener_fv(self, param, values) -> None:
        self.set()
        al.alListenerfv(param, values)

    def sample_audio(self) -> List[List]:
        self.set()
        audio_data_type = ctypes.c_float * SAMPLE_SIZE * 2
        audio_sample = audio_data_type()
        audio_sample_pointer = ctypes.cast(audio_sample, ctypes.c_void_p)

        alc.alcRenderSamplesSOFT(self.device, audio_sample_pointer, al.ALsizei(SAMPLE_SIZE))
        sampled_audio = list(ctypes.cast(audio_sample_pointer, ctypes.POINTER(audio_data_type)).contents)
        separated_channel_audio = [[], []]
        for i in range(SAMPLE_SIZE):
            separated_channel_audio[0].append(sampled_audio[0][i])
            separated_channel_audio[1].append(sampled_audio[1][i])
        return separated_channel_audio
