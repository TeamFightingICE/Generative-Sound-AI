from loguru import logger
from pyftg.models.frame_data import FrameData

from src.sound_manager import SoundManager
from src.config import STAGE_HEIGHT, STAGE_WIDTH


class CharacterPlay:
    character = None
    sound_manager = None
    source_default = None
    source_walking = None
    source_landing = None
    source_project_tiles = [None] * 3
    source_energy_change = None
    source_border_alert = None
    source_heart_beat = None

    temp = None
    temp2 = None
    pre_energy = 0

    projectile_live = [False] * 3
    projectile_hit = [False] * 3
    sY = [0] * 3
    sX = [0] * 3
    player = None

    def __init__(self, sound_manager: SoundManager, player: bool) -> None:
        # self.character = character
        self.sound_manager = sound_manager
        self.player = player
        self.update_projectile()

    def update_projectile(self):
        # self.character.
        # TODO
        pass

    def update(self, frame_data: FrameData):
        self.character = frame_data.get_character(self.player)
        # check landing
        if self.character.bottom >= STAGE_HEIGHT:
            pass
            # TODO
        
        # border
        if self.player:
            logger.info(f"left: {self.character.left}, right: {self.character.right}")
        if self.character.left < 0 or self.character.right > STAGE_WIDTH:
            logger.info("border")
            if not self.sound_manager.is_playing(self.source_border_alert):
                if self.character.left < 0:
                    self.sound_manager.play(self.source_border_alert, self.sound_manager.get_buffer("BorderAlert.wav"), 0, 0, False)
                else:
                    self.sound_manager.play(self.source_border_alert, self.sound_manager.get_buffer("BorderAlert.wav"), STAGE_WIDTH, 0, False)

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

    