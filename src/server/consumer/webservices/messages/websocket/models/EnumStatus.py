from enum import IntFlag, auto


class EnumStatus(IntFlag):
    NONE = 0
    HIT = auto()
    SHOOTING = auto()
    SHIELD_SHOW = auto()
    SHIELD_HIDE = auto()

