from loguru import logger
from pyftg.aiinterface.sound_ai_interface import SoundAIInterface
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.round_result import RoundResult
from typing import List

from character_play import CharacterPlay
from sound_manger import SoundManager

class SoundAI(SoundAIInterface):
    character_plays: List[CharacterPlay] = []
    sound_manager: SoundManager = None

    def __init__(self):
        self.audio_sample_bytes = bytes(8192)
        self.sound_manager = SoundManager()

    def initialize(self, game_data: GameData):
        logger.info("initialize")
        self.character_plays[0] = CharacterPlay(self.sound_manager, False)
        self.character_plays[1] = CharacterPlay(self.sound_manager, True)

    def processing_game(self, frame_data: FrameData):
        logger.info("processing game")
        self.character_plays[0].update(frame_data)
        self.character_plays[1].update(frame_data)

    def round_end(self, round_result: RoundResult):
        logger.info("round end")

    def game_end(self):
        logger.info("game end")

    def audio_sample(self) -> bytes:
        self.audio_sample_bytes = self.sound_manager.render_sound()
        return self.audio_sample_bytes