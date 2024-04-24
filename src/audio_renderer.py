class SoundRenderer:
    device = None
    context = None
    
    def __init__(self, device, context) -> None:
        self.device = device
        self.context = context

    def set(self):
        pass
    
    def play(self, source_id: int, buffer_id: int) -> None:
        self.set()

    def stop(self, source_id: int):
        set()

    def play(self, source_id: int, buffer_id: int, x: int, y: int, loop: bool) -> None:
        pass

    def set_source_gain(self, source_id: int, gain: float) -> None:
        set()
        
    def set_source_3f(self, source_id: int, param, x: int, y: int, z: int) -> None:
        set()
        
    def delete_source(self, source_id: int) -> None:
        pass

    def delete_buffer(self, buffer_id: int) -> None:
        pass

    def close(self):
        set()

    def is_playing(self, source_id: int) -> bool:
        pass

    def al_listener_fv(self, param, values) -> None:
        pass

    def sample_audio() -> bytes:
        return None
