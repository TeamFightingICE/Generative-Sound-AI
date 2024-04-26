from loguru import logger
from pyftg.models.frame_data import FrameData, CharacterData
from pyftg.models.attack_data import AttackData
from typing import List

from src.sound_manager import SoundManager
from src.config import STAGE_HEIGHT, STAGE_WIDTH
from src.audio_source import AudioSource


class CharacterPlay:
    character: CharacterData
    opp_character: CharacterData
    sound_manager: SoundManager
    source_default: AudioSource
    source_walking: AudioSource
    source_landing: AudioSource
    source_project_tiles: List[AudioSource]
    source_energy_change: AudioSource
    source_border_alert: AudioSource
    source_heart_beat: AudioSource
    temp: str
    temp2: str
    pre_energy: int
    projectile_live: List[bool]
    projectile_hit: List[bool]
    projectile_attack: List[AttackData]
    sY: List[int]
    sX: List[int]
    player: bool
    previous_left: int
    previous_bottom: int


    def __init__(self, sound_manager: SoundManager, player: bool) -> None:
        # self.character = character
        self.character = None
        self.opp_character = None
        self.sound_manager = sound_manager
        self.source_default = sound_manager.create_source()
        self.source_walking = sound_manager.create_source()
        self.source_landing = sound_manager.create_source()
        self.source_project_tiles = [sound_manager.create_source()] * 3
        self.source_energy_change = sound_manager.create_source()
        self.source_border_alert = sound_manager.create_source()
        self.source_heart_beat = sound_manager.create_source()

        self.temp = None
        self.temp2 = None
        self.pre_energy = 0

        self.projectile_live = [False] * 3
        self.projectile_hit = [False] * 3
        self.sY = [0] * 3
        self.sX = [0] * 3
        self.player = player
        self.previous_left = -1
        self.previous_bottom = -1
        self.projectile_live = [False] * 3
        self.projectile_hit = [False] * 3
        self.projectile_attack = [None] * 3

        self.update_projectile()
        self.count = 0
        

    def update_projectile(self):
        # self.character.
        for i in range(len(self.projectile_attack)):
            if self.projectile_attack[i] is not None:
                if self.projectile_live[i]:
                    if self.projectile_attack[i].current_frame <= self.projectile_attack[i].active:
                        self.sX[i] += self.projectile_attack[i].speed_x
                        self.sY[i] += self.projectile_attack[i].speed_y
                        self.sound_manager.set_source_pos(self.source_project_tiles[i], self.sX[i], self.sY[i])
                    else:
                        self.sound_manager.stop(self.source_project_tiles[i])
            elif self.source_project_tiles is not None:
                self.sound_manager.stop(self.source_project_tiles[i])

        # pass

    def update(self, frame_data: FrameData):
        
        self.count += 1
        self.character = frame_data.get_character(self.player)
        self.opp_character = frame_data.get_character(not self.player)

        if self.detection_hit(self.opp_character):
            # check guard
            if self.is_guard(self.opp_character.attack_data):
                self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("WeakGuard.wav"), self.character.x, self.character.y, False)
            else:
                # check being hit
                if self.opp_character.attack_data.attack_type != 4:
                    if self.opp_character.attack_data.down_prop:
                        self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("HitB.wav"), self.character.x, self.character.y, False)
                    else:
                        self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("HitA.wav"), self.character.x, self.character.y, False)


        # check landing
        if self.previous_bottom == -1:
            self.previous_bottom = self.character.bottom
        if self.character.bottom >= STAGE_HEIGHT and self.character.bottom != self.previous_bottom:
            self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("LANDING.wav"), self.character.x, self.character.y, False)
        self.previous_bottom = self.character.bottom
            
        
        # border
        # if self.player:
            # logger.info(f"left: {self.character.left}, right: {self.character.right}")
        if self.previous_left == -1:
            self.previous_left = self.character.left
        if (self.character.left == 0 and self.previous_left > 0) or self.character.right > STAGE_WIDTH:
            logger.info("border")
            if not self.sound_manager.is_playing(self.source_border_alert):
                if self.character.left < 0:
                    self.sound_manager.play(self.source_border_alert, self.sound_manager.get_buffer("BorderAlert.wav"), 0, 0, False)
                else:
                    self.sound_manager.play(self.source_border_alert, self.sound_manager.get_buffer("BorderAlert.wav"), STAGE_WIDTH, 0, False)
        self.previous_left = self.character.left

        # hp
        if self.character.hp < 50:
            if not self.sound_manager.is_playing(self.source_heart_beat):
                if self.player:
                    self.sound_manager.play(self.source_heart_beat, self.sound_manager.get_buffer("Heartbeat.wav"), 0, 0, False)
                else:
                    self.sound_manager.play(self.source_heart_beat, self.sound_manager.get_buffer("Heartbeat.wav"), STAGE_WIDTH, 0, False)

        # update temp
        if self.character.state.name != "CROUCH":
            self.temp = " "
        if self.character.speed_x == 0 and self.character.state == "AIR":
            self.temp2 = " "
            self.sound_manager.stop(self.source_walking)
        else:
            self.sound_manager.set_source_pos(self.source_walking, self.character.x, self.character.y)

        self.update_projectile()
        # update energy
        if self.character.energy > self.pre_energy + 50:
            self.pre_energy = self.character.energy
            if self.player:
                self.sound_manager.play(self.source_energy_change, self.sound_manager.get_buffer("EnergyCharge.wav"), 0, 0, False)
            else:
                self.sound_manager.play(self.source_energy_change, self.sound_manager.get_buffer("EnergyCharge.wav"), STAGE_WIDTH, 0, False)

        self.play_action_sound()
        

    def play_action_sound(self):
        # get action
        action = self.character.action.name
        sound_name = action + '.wav'
        x = self.character.x
        y = self.character.y
        
        if action in ["JUMP", "FOR_JUMP", "BACK_JUMP", "THROW_A", "THROW_B", "THROW_HIT", "THROW_SUFFER", 
                      "STAND_A", "STAND_B", "CROUCH_A", "CROUCH_B", "AIR_A", "AIR_B", "AIR_DA", "AIR_DB", 
                      "STAND_FA", "STAND_FB", "CROUCH_FA", "CROUCH_FB", "AIR_FA", "AIR_FB", "AIR_UA", "AIR_UB", 
                      "STAND_F_D_DFA", "STAND_F_D_DFB", "STAND_D_DB_BA", "STAND_D_DB_BB", "AIR_F_D_DFA", 
                      "AIR_F_D_DFB", "AIR_D_DB_BA", "AIR_D_DB_BB"]:
            self.sound_manager.play(self.source_default, self.sound_manager.get_buffer(sound_name), x, y, False)
        elif action == "CROUCH":
            if sound_name != self.temp:
                self.sound_manager.play(self.source_default, self.sound_manager.get_buffer(sound_name), x, y, False)
                self.temp = sound_name
        elif action in ["STAND_D_DF_FA", "STAND_D_DF_FB", "AIR_D_DF_FA", "AIR_D_DF_FB", "STAND_D_DF_FC"]:
            for i in range(len(self.projectile_live)):
                if not self.projectile_live[i]:
                    self.projectile_live[i] = True
                    self.sY[i] = y
                    self.sX[i] = x
                    self.sound_manager.play(self.source_project_tiles[i], self.sound_manager.get_buffer(sound_name), x, y, True)
                    break

    def round_end(self):
        self.pre_energy = 0
        self.temp = None
        self.temp2 = None
        self.sY = [0] * 3
        self.sX = [0] * 3
        self.previous_left = -1
        self.previous_bottom = -1
        

    def detection_hit(self, opponent: CharacterData) ->bool:
        if self.character.attack_data is None or opponent.state.name == 'DOWN':
            return False
        elif self.character.left <= opponent.attack_data.current_hit_area.right and\
                self.character.right >= opponent.attack_data.current_hit_area.left and\
                self.character.top <= opponent.attack_data.current_hit_area.bottom and\
                self.character.bottom >= opponent.attack_data.current_hit_area.top:
            return True
        return False

    def is_guard(self, attack: AttackData) -> bool:
        # guard = False
        action = self.character.action.name
        if action == "STAND_GUARD":
            if attack.attack_type in [1, 2]:
                return True
        if action == "CROUCH_GUARD":
            if attack.attack_type in [1, 3]:
                return True
        if action == "AIR_GUARD":
            if attack.attack_type in [1, 2]:
                return True
        if action == "STAND_GUARD_RECOV":
            return True
        if action == "CROUCH_GUARD_RECOV":
            return True
        if action == "AIR_GUARD_RECOV":
            return True
        return False

    