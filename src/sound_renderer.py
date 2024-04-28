import ctypes

from openal import al, alc


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

    def sample_audio() -> bytes:
        return None
