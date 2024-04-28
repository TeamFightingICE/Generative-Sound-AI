from typing import List

from pyftg.aiinterface.soundgenai_interface import SoundGenAIInterface
from pyftg.models.frame_data import FrameData
from pyftg.models.game_data import GameData
from pyftg.models.round_result import RoundResult

from src.character_play import CharacterPlay
from src.sound_manager import SoundManager
from src.utils import detection_hit


class SampleSoundGenAI(SoundGenAIInterface):
    sound_manager: SoundManager = SoundManager.get_instance()
    character_plays: List[CharacterPlay] = []

    def __init__(self):
        self.character_plays.append(CharacterPlay(True))
        self.character_plays.append(CharacterPlay(False))

    def initialize(self, game_data: GameData):
        pass

    def init_round(self):
        print("play BGM")

    def processing_game(self, frame_data: FrameData):
        for i in range(2):
            player_number = i == 0
            opponent_index = 1 if player_number else 0
            attack = frame_data.get_character(player_number).attack_data
            if detection_hit(frame_data.get_character(not player_number), attack):
                self.character_plays[i].hit_attack(attack, self.character_plays[opponent_index])

            self.character_plays[i].update(frame_data)

    def round_end(self, round_result: RoundResult):
        print("stop BGM")
        for i in range(2):
            self.character_plays[i].reset()

    def game_end(self):
        pass

    def audio_sample(self) -> bytes:
        return self.sound_manager.render_sound()
