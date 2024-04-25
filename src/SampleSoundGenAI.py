from typing import List

from loguru import logger
from pyftg.aiinterface.sound_ai_interface import SoundAIInterface
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.round_result import RoundResult

from src.character_play import CharacterPlay
from src.sound_manager import SoundManager


class SampleSoundGenAI(SoundAIInterface):

    def __init__(self):
        self.character_plays: List[CharacterPlay] = []
        self.audio_sample_bytes: bytes = None
        self.sound_manager = SoundManager.get_instance()

    def initialize(self, game_data: GameData):
        self.character_plays.append(CharacterPlay(self.sound_manager, True))
        self.character_plays.append(CharacterPlay(self.sound_manager, False))

    def processing_game(self, frame_data: FrameData):
        self.character_plays[0].update(frame_data)
        self.character_plays[1].update(frame_data)

    def round_end(self, round_result: RoundResult):
        pass

    def game_end(self):
        pass

    def audio_sample(self) -> bytes:
        self.audio_sample_bytes = self.sound_manager.render_sound()
        return self.audio_sample_bytes