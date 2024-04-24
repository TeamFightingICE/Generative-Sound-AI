
class SoundRenderer:
    device = None
    context = None
    
    def __init__(self, device, context) -> None:
        self.device = device
        self.context = context

    def set(self):
        pass
    
    def play(self, source_id, buffer_id):
        self.set()

    def stop(self, source_id):
        set()
        

    def play(self, source_id, buffer_id, x, y, loop):
        pass

    def set_source_gain(self, source_id, gain):
        set()
        

    def set_source_3f(self, source_id, param, x, y, z):
        set()
        
    
    def delete_source(self, source_id):
        pass

    def delete_buffer(self, buffer_id):
        pass

    def close(self):
        set()
        

    def is_playing(self, source_id):
        pass

    def al_listener_fv(self, param, values):
        pass

    def sample_audio():
        return None