from typing import List

from pyftg.models.attack_data import AttackData
from pyftg.models.enums.action import Action
from pyftg.models.enums.state import State
from pyftg.models.frame_data import CharacterData, FrameData

from src.audio_source import AudioSource
from src.config import STAGE_HEIGHT, STAGE_WIDTH
from src.sound_manager import SoundManager
from src.utils import is_guard


class CharacterPlay:
    sound_manager: SoundManager = SoundManager.get_instance()

    temp: str = ' '
    temp2: str = ' '
    temp3: str = ' '
    temp4: str = ' '
    pre_energy: int = 0
    previous_left: int = -1
    previous_bottom: int = -1
    previous_action: str = None
    heart_beat_flag: bool = False
    projectile_live: List[bool] = [False] * 3

    player: bool
    character: CharacterData
    opp_character: CharacterData
    source_default: AudioSource
    source_walking: AudioSource
    source_landing: AudioSource
    source_projectiles: List[AudioSource]
    source_energy_change: AudioSource
    source_border_alert: AudioSource
    source_heart_beat: AudioSource

    def __init__(self, player: bool) -> None:
        self.player = player
        self.source_default = self.sound_manager.create_source()
        self.source_walking = self.sound_manager.create_source()
        self.source_landing = self.sound_manager.create_source()
        self.source_projectiles = [self.sound_manager.create_source()] * 3
        self.source_energy_change = self.sound_manager.create_source()
        self.source_border_alert = self.sound_manager.create_source()
        self.source_heart_beat = self.sound_manager.create_source()

    def update_projectile(self):
        projectile_attack = self.character.projectile_attack
        projectile_live = self.character.projectile_live
        for i in range(len(projectile_attack)):
            if not projectile_attack[i].empty_flag and projectile_live[i]:
                x = (projectile_attack[i].current_hit_area.left + projectile_attack[i].current_hit_area.right) // 2
                y = (projectile_attack[i].current_hit_area.top + projectile_attack[i].current_hit_area.bottom) // 2
                self.sound_manager.set_source_pos(self.source_projectiles[i], x, y)
            elif not projectile_live[i] and self.sound_manager.is_playing(self.source_projectiles[i]):
                self.sound_manager.stop(self.source_projectiles[i])
            self.projectile_live[i] = projectile_live[i]

    def hit_attack(self, attack: AttackData, opponent: 'CharacterPlay') -> None:
        if is_guard(self.character.action, attack):  # check guard
            self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("WeakGuard.wav"), self.character.x, self.character.y, False)
        else:
            # check being hit
            if attack.attack_type == 4:
                if self.character.state not in [State.AIR, State.DOWN]:
                    self.run_action(Action.THROW_SUFFER)
                    if not self.opp_character.action is Action.THROW_SUFFER:
                        opponent.run_action(Action.THROW_HIT)
            else:
                if attack.down_prop:
                    self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("HitB.wav"), self.character.x, self.character.y, False)
                else:
                    self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("HitA.wav"), self.character.x, self.character.y, False)

    def run_action(self, action: Action) -> None:
        action_name = action.name.upper()
        sound_name = action_name + '.wav'
        x = self.character.x
        y = self.character.y

        if action in [Action.STAND, Action.AIR]:
            self.temp = ' '
            self.temp2 = ' '
            self.temp3 = ' '
            self.temp4 = ' '
        
        if action_name in ["JUMP", "FOR_JUMP", "BACK_JUMP", "THROW_A", "THROW_B", "THROW_HIT", "THROW_SUFFER", 
                      "STAND_A", "STAND_B", "CROUCH_A", "CROUCH_B", "AIR_A", "AIR_B", "AIR_DA", "AIR_DB", 
                      "STAND_FA", "STAND_FB", "CROUCH_FA", "CROUCH_FB", "AIR_FA", "AIR_FB", "AIR_UA", "AIR_UB", 
                      "STAND_F_D_DFA", "STAND_F_D_DFB", "STAND_D_DB_BA", "STAND_D_DB_BB", "AIR_F_D_DFA", 
                      "AIR_F_D_DFB", "AIR_D_DB_BA", "AIR_D_DB_BB"]:
            if sound_name != self.temp3:
                self.sound_manager.play(self.source_default, self.sound_manager.get_buffer(sound_name), x, y, False)
                self.temp3 = sound_name
        elif action_name == "CROUCH":
            if sound_name != self.temp:
                self.sound_manager.play(self.source_default, self.sound_manager.get_buffer(sound_name), x, y, False)
                self.temp = sound_name
        elif action_name in ["FORWARD_WALK", "DASH", "BACK_STEP"]:
            if sound_name != self.temp2:
                self.sound_manager.play(self.source_walking, self.sound_manager.get_buffer(sound_name), x, y, True)
                self.temp2 = sound_name
        elif action_name in ["STAND_D_DF_FA", "STAND_D_DF_FB", "AIR_D_DF_FA", "AIR_D_DF_FB", "STAND_D_DF_FC"]:
            if sound_name != self.temp4:
                for i in range(len(self.character.projectile_live)):
                    if not self.character.projectile_live[i]:
                        self.sound_manager.play(self.source_projectiles[i], self.sound_manager.get_buffer(sound_name), x, y, True)
                        break
                self.temp4 = sound_name

        self.previous_action = action
    
    def check_landing(self):
        if self.previous_bottom == -1:
            self.previous_bottom = self.character.bottom
        if self.character.bottom >= STAGE_HEIGHT and self.character.bottom != self.previous_bottom:
            self.sound_manager.play(self.source_landing, self.sound_manager.get_buffer("LANDING.wav"), self.character.x, self.character.y, False)
        self.previous_bottom = self.character.bottom

    def check_border_alert(self):
        if self.previous_left == -1:
            self.previous_left = self.character.left
        if (self.character.left == 0 and self.previous_left > 0) or self.character.right > STAGE_WIDTH:
            if not self.sound_manager.is_playing(self.source_border_alert):
                if self.character.left < 0:
                    self.sound_manager.play(self.source_border_alert, self.sound_manager.get_buffer("BorderAlert.wav"), 0, 0, False)
                else:
                    self.sound_manager.play(self.source_border_alert, self.sound_manager.get_buffer("BorderAlert.wav"), STAGE_WIDTH, 0, False)
        self.previous_left = self.character.left

    def check_heart_beat(self):
        if self.character.hp < 50 and not self.heart_beat_flag:
            self.heart_beat_flag = True
            if not self.sound_manager.is_playing(self.source_heart_beat):
                if self.player:
                    self.sound_manager.play(self.source_heart_beat, self.sound_manager.get_buffer("Heartbeat.wav"), 0, 0, False)
                else:
                    self.sound_manager.play(self.source_heart_beat, self.sound_manager.get_buffer("Heartbeat.wav"), STAGE_WIDTH, 0, False)

    def check_energy_charge(self):
        if self.character.energy > self.pre_energy + 50:
            self.pre_energy = self.character.energy
            if self.player:
                self.sound_manager.play(self.source_energy_change, self.sound_manager.get_buffer("EnergyCharge.wav"), 0, 0, False)
            else:
                self.sound_manager.play(self.source_energy_change, self.sound_manager.get_buffer("EnergyCharge.wav"), STAGE_WIDTH, 0, False)
    
    def update(self, frame_data: FrameData):
        self.character = frame_data.get_character(self.player)
        self.opp_character = frame_data.get_character(not self.player)

        self.check_landing()
        self.check_border_alert()
        self.check_heart_beat()
        self.check_energy_charge()

        # update temp
        if not self.character.state is State.CROUCH:
            self.temp = " "
        if self.character.speed_x == 0 and self.character.state is State.AIR:
            self.temp2 = " "
            if self.sound_manager.is_playing(self.source_walking):
                self.sound_manager.stop(self.source_walking)
        else:
            self.sound_manager.set_source_pos(self.source_walking, self.character.x, self.character.y)

        self.run_action(self.character.action)
        self.update_projectile()

    def reset(self):
        self.pre_energy = 0
        self.temp = ' '
        self.temp2 = ' '
        self.temp3 = ' '
        self.temp4 = ' '
        self.previous_left = -1
        self.previous_bottom = -1
        self.heart_beat_flag = False
    