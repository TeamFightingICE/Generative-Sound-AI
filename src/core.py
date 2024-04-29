from typing import List

from pyftg.aiinterface.soundgenai_interface import SoundGenAIInterface
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.round_result import RoundResult

from src.audio_source import AudioSource
from src.character_play import CharacterPlay
from src.config import ENABLE_VIRTUAL_AUDIO
from src.sound_manager import SoundManager
from src.utils import detection_hit


class SampleSoundGenAI(SoundGenAIInterface):
    sound_manager: SoundManager = SoundManager.get_instance()
    source_bgm: AudioSource = sound_manager.create_audio_source()
    character_plays: List[CharacterPlay] = []

    def __init__(self):
        self.character_plays.append(CharacterPlay(player=True))
        self.character_plays.append(CharacterPlay(player=False))

    def initialize(self, game_data: GameData):
        pass

    def init_round(self):
        self.sound_manager.set_source_gain(self.source_bgm, 1.0)
        self.sound_manager.play(self.source_bgm, self.sound_manager.get_sound_buffer("BGM0.wav"), 350, 0, True)

    def processing_game(self, frame_data: FrameData):
        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            projectiles = frame_data.get_character(player_number).projectile_attack
            for p in projectiles:
                if detection_hit(frame_data.get_character(not player_number), p):
                    self.character_plays[i].hit_attack(p, self.character_plays[opponent_index])
        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            attack = frame_data.get_character(player_number).attack_data
            if detection_hit(frame_data.get_character(not player_number), attack):
                self.character_plays[i].hit_attack(attack, self.character_plays[opponent_index])

            self.character_plays[i].update(frame_data)

    def round_end(self, round_result: RoundResult):
        for i in range(2):
            self.character_plays[i].reset()
        self.sound_manager.stop(self.source_bgm)
        self.sound_manager.stop_all()

    def game_end(self):
        self.sound_manager.close()

    def audio_sample(self) -> bytes:
        if ENABLE_VIRTUAL_AUDIO:
            sample = self.sound_manager.render_sound()
        else:
            sample = bytes(8192)
        return sample
