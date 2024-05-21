import logging

from pyftg.aiinterface.ai_interface import AIInterface
from pyftg.models.audio_data import AudioData
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.key import Key
from pyftg.models.round_result import RoundResult
from pyftg.models.screen_data import ScreenData

logger = logging.getLogger(__name__)


class TestAudio(AIInterface):
    def __init__(self):
        self.blind_flag = True

    def name(self) -> str:
        return self.__class__.__name__

    def is_blind(self) -> bool:
        return self.blind_flag

    def initialize(self, game_data: GameData, player: bool):
        logger.info("initialize")
        self.input_key = Key()
        self.player = player

    def get_non_delay_frame_data(self, frame_data: FrameData):
        self.frame = frame_data.current_frame_number
        
    def input(self):
        return self.input_key
        
    def get_information(self, frame_data: FrameData, is_control: bool):
        # self.frame = frame_data.current_frame_number
        pass
    
    def get_screen_data(self, screen_data: ScreenData):
        pass
    
    def get_audio_data(self, audio_data: AudioData):
        print("get_audio_data() called at", self.frame, "with data", audio_data.raw_data_bytes[:10])
        
    def processing(self):
        pass

    def round_end(self, round_result: RoundResult):
        logger.info(f"round end: {round_result}")
    
    def game_end(self):
        logger.info("game end")

    def close(self):
        pass