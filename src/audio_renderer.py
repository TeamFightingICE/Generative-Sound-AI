from openal import alc, al
class SoundRenderer:
    device = None
    context = None
    
    def __init__(self, device, context) -> None:
        self.device = device
        self.context = context

    def set(self):
        alc.alcMakeContextCurrent(self.context)
    
    def play(self, source_id, buffer_id):
        self.set()
        al.alSourcei(source_id, al.AL_BUFFER, buffer_id)
        al.alSourcePlay(source_id)

    def stop(self, source_id):
        set()
        al.alSourceStop(source_id)

    def play(self, source_id, buffer_id, x, y, loop):
        pass

    def set_source_gain(self, source_id, gain):
        set()
        al.alSourcef(source_id, al.AL_GAIN, gain)

    def set_source_3f(self, source_id, param, x, y, z):
        set()
        al.alSource3f(source_id, param, x, y, z)
    
    def delete_source(self, source_id):
        pass

    def delete_buffer(self, buffer_id):
        pass

    def close(self):
        set()
        alc.alcDestroyContext(self.context)
        alc.alcCloseDevice(self.device)

    def is_playing(self, source_id):
        pass

    def al_listener_fv(self, param, values):
        pass

    def sample_audio():
        return None