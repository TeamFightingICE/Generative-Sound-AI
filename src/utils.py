from pathlib import Path

from loguru import logger
from pyftg.models.attack_data import AttackData
from pyftg.models.character_data import CharacterData
from pyftg.models.enums.action import Action
from pyftg.models.enums.state import State

from src.config import ENABLE_LOGGING


def setup_logging():
    if ENABLE_LOGGING:
        Path("logs").mkdir(exist_ok=True)
        logger.add("logs/{time}.log")
    else:
        logger.disable("")


def detection_hit(opponent: CharacterData, attack: AttackData) ->bool:
    if not attack or opponent.state is State.DOWN:
        return False
    else:
        return (opponent.left <= attack.current_hit_area.right and opponent.right >= attack.current_hit_area.left and 
                opponent.top <= attack.current_hit_area.bottom and opponent.bottom >= attack.current_hit_area.top)


def is_guard(action: Action, attack: AttackData) -> bool:
    if action is Action.STAND_GUARD:
        if attack.attack_type in [1, 2]:
            return True
    if action is Action.CROUCH_GUARD:
        if attack.attack_type in [1, 3]:
            return True
    if action is Action.AIR_GUARD:
        if attack.attack_type in [1, 2]:
            return True
    if action is Action.STAND_GUARD_RECOV:
        return True
    if action is Action.CROUCH_GUARD_RECOV:
        return True
    if action is Action.AIR_GUARD_RECOV:
        return True
    return False