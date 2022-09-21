from enum import IntFlag, auto


class EnumStatus(IntFlag):
    HIT = auto(1)
    SHOOTING = auto(2)
    SHIELD_SHOW = auto(3)
    SHIELD_HIDE = auto(4)
