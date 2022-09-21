from enum import IntFlag, auto


class EnumStatus(IntFlag):
    NONE = 0
    HIT = auto()
    SHOOTING = auto()
    SHIELD_SHOW = auto()
    SHIELD_HIDE = auto()



if EnumStatus.NONE in action:
    print(EnumStatus.SHOOTING.value)
    print(EnumStatus.HIT.value)
    print(EnumStatus.SHIELD_SHOW.value)
    print(EnumStatus.SHIELD_HIDE.value)
    print("hit")
