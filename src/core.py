from typing import List

from loguru import logger
from pyftg.aiinterface.soundgenai_interface import SoundGenAIInterface
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.round_result import RoundResult
from pyftg_sound.models.audio_source import AudioSource
from pyftg_sound.models.sound_renderer import SoundRenderer
from pyftg_sound.sound_manager import SoundManager

from src.character_audio_handler import CharacterAudioHandler
from src.config import (BGM_VOLUME, DATA_PATH, ENABLE_AUDIO_OUTPUT,
                        SOUND_RENDER_SIZE, SOUND_SAMPLE_RATE, STAGE_HEIGHT,
                        STAGE_WIDTH)
from src.constants import source_attrs
from src.utils import detection_hit


class SampleSoundGenAI(SoundGenAIInterface):
    sound_manager: SoundManager
    source_bgm: AudioSource
    character_handlers: List[CharacterAudioHandler] = []

    def __init__(self):
        self.sound_manager = SoundManager()
        virtual_renderer = SoundRenderer.create_virtual_renderer(sample_rate=SOUND_SAMPLE_RATE)
        self.sound_manager.set_virtual_renderer(virtual_renderer)
        if ENABLE_AUDIO_OUTPUT:
            default_renderer = SoundRenderer.create_default_renderer()
            self.sound_manager.set_default_renderer(default_renderer)
        self.sound_manager.set_listener_position(STAGE_WIDTH / 2, 0, STAGE_HEIGHT / 2)
        self.sound_manager.set_listener_orientation(0, 0, -1, 0, 1, 0)
        logger.info("Sound manager has been initialized.")

        for file in DATA_PATH.iterdir():
            self.sound_manager.create_audio_buffer(file)
        logger.info("Sound effects have been loaded.")

        self.source_bgm = self.sound_manager.create_audio_source(source_attrs)
        self.sound_manager.set_source_gain(self.source_bgm, BGM_VOLUME)
        self.character_handlers.append(CharacterAudioHandler(self.sound_manager, True))
        self.character_handlers.append(CharacterAudioHandler(self.sound_manager, False))

    def initialize(self, game_data: GameData):
        logger.info("Initialize")

    def get_information(self, frame_data: FrameData):
        self.frame_data = frame_data

    def processing(self):
        if self.frame_data.empty_flag or self.frame_data.current_frame_number < 0:
            return

        if self.frame_data.current_frame_number == 0:
            self.sound_manager.play(self.source_bgm, self.sound_manager.get_sound_buffer("BGM0.wav"), STAGE_WIDTH // 2, STAGE_HEIGHT // 2, True)
            logger.info(f"Play sound: BGM0.wav at ({STAGE_WIDTH // 2}, {STAGE_HEIGHT // 2}) with loop=True")

        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            projectiles = self.frame_data.get_character(player_number).projectile_attack
            for p in projectiles:
                if detection_hit(self.frame_data.get_character(not player_number), p):
                    self.character_handlers[i].hit_attack(p, self.character_handlers[opponent_index])

        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            attack = self.frame_data.get_character(player_number).attack_data
            if detection_hit(self.frame_data.get_character(not player_number), attack):
                self.character_handlers[i].hit_attack(attack, self.character_handlers[opponent_index])

            self.character_handlers[i].update(self.frame_data)

    def round_end(self, round_result: RoundResult):
        logger.info("Round end")
        for i in range(2):
            self.character_handlers[i].reset()
        self.sound_manager.stop(self.source_bgm)
        self.sound_manager.stop_all()
        logger.info("Stop all sound")

    def game_end(self):
        logger.info("Game end")

    def audio_sample(self) -> bytes:
        audio_sample = self.sound_manager.sample_audio(render_size=SOUND_RENDER_SIZE)
        return audio_sample.tobytes()
    
    def close(self):
        self.sound_manager.close()
        logger.info("Close sound manager")
