from abc import ABC


class IMoving(ABC):

    @property
    def is_moving(self) -> bool:
        """
        Is the entity moving?
        """
        return self._is_moving

    @property
    def moving_speed(self) -> float:
        """
        Speed in point per seconds.
        """
        return self._moving_speed

    @property
    def is_turning(self) -> bool:
        """
        Is the entity turning?
        """
        return self._is_turning

    @property
    def turn_direction(self) -> str:
        """
        Is the entity turning?
        """
        return self._turn_direction

    @property
    def turning_speed(self) -> float:
        """
        Rotating speed in radians per seconds.
        """
        return self._turning_speed

    def __init__(self, moving_speed: float = 1.0, turning_speed: float = 0.1):
        self._is_moving = False
        self._is_turning = False
        self._turn_direction = str()
        self._moving_speed = moving_speed
        self._turning_speed = turning_speed

        # Last entity move timestamp
        self.last_move_timestamp = 0.0

        # Last entity turn timestamp
        self.last_turn_timestamp = 0.0

    def set_moving(self, state: bool):
        """
        Set the entity to moving or stopped.
        """
        self.last_move_timestamp = 0.0
        self._is_moving = state

    def set_turning(self, state: bool, direction: str = str()):
        """
        Set the entity to turn or go straight.
        """
        self.last_turn_timestamp = 0.0
        self._is_turning = state
        self._turn_direction = direction

    @staticmethod
    def get_distance_from_time_and_speed(moving_speed: float, elapsed_time_secs: float) -> float:
        """
        Return the traveled distance for an amount of time.
        """
        return moving_speed * elapsed_time_secs

    @staticmethod
    def get_turn_from_time_and_speed(turning_speed: float, elapsed_time_secs: float) -> float:
        """
        Return the rotation in radians for an amount of time.
        """
        return turning_speed * elapsed_time_secs
