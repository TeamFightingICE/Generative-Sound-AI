from typing import List

from loguru import logger
from pyftg.aiinterface.soundgenai_interface import SoundGenAIInterface
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.round_result import RoundResult

from src.audio_source import AudioSource
from src.character_audio_handler import CharacterAudioHandler
from src.config import ENABLE_VIRTUAL_AUDIO, STAGE_WIDTH
from src.sound_manager import SoundManager
from src.utils import detection_hit


class SampleSoundGenAI(SoundGenAIInterface):
    sound_manager: SoundManager
    source_bgm: AudioSource
    character_handlers: List[CharacterAudioHandler] = []

    def __init__(self):
        self.sound_manager = SoundManager.get_instance()
        self.source_bgm = self.sound_manager.create_audio_source()
        self.character_handlers.append(CharacterAudioHandler(player=True))
        self.character_handlers.append(CharacterAudioHandler(player=False))

    def initialize(self, game_data: GameData):
        logger.info("Initialize")

    def init_round(self):
        self.sound_manager.set_source_gain(self.source_bgm, 1.0)
        self.sound_manager.play(self.source_bgm, self.sound_manager.get_sound_buffer("BGM0.wav"), STAGE_WIDTH // 2, 0, True)
        logger.info(f"Play sound: BGM0.wav at ({STAGE_WIDTH // 2}, 0) with loop=True")

    def processing_game(self, frame_data: FrameData):
        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            projectiles = frame_data.get_character(player_number).projectile_attack
            for p in projectiles:
                if detection_hit(frame_data.get_character(not player_number), p):
                    self.character_handlers[i].hit_attack(p, self.character_handlers[opponent_index])

        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            attack = frame_data.get_character(player_number).attack_data
            if detection_hit(frame_data.get_character(not player_number), attack):
                self.character_handlers[i].hit_attack(attack, self.character_handlers[opponent_index])

            self.character_handlers[i].update(frame_data)

    def round_end(self, round_result: RoundResult):
        for i in range(2):
            self.character_handlers[i].reset()
        self.sound_manager.stop(self.source_bgm)
        self.sound_manager.stop_all()
        logger.info("Stop all sound")

    def game_end(self):
        logger.info("Game end")

    def audio_sample(self) -> bytes:
        if ENABLE_VIRTUAL_AUDIO:
            audio_sample = self.sound_manager.sample_audio()
            return audio_sample.tobytes()
        return bytes(6400)
    
    def close(self):
        self.sound_manager.close()
        logger.info("Close sound manager")
