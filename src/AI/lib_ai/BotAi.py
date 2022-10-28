from utils.rest import Rest, RestException
from ConnectionManager import ConnectionManager


class BotAi:

    RestException: RestException = RestException

    @property
    def bot_id(self):
        return self.connection_manager.bot_id

    def __init__(self, bot_name: str, team_id: str):
        self._bot_name = bot_name
        self._team_id = team_id
        self.connection_manager = ConnectionManager()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Close threads.
        """
        self.connection_manager.close()

    def enroll(self, bot_id: str = str()) -> str:
        """
        Enroll or re-enroll a bot on the server.
        """
        return self.connection_manager.enroll_new_bot(self._bot_name, self._team_id, bot_id)

    def read_scanner(self) -> dict:
        """
        Read and remove one item from the scanner queue.
        """
        return self.connection_manager.mqtt_queue.get()

    def read_game_message(self):
        """
        Read and remove one item from the game messages queue.
        """
        return self.connection_manager.stomp_queue.get()

    def move(self, state):
        """
        Start or stop moving the bot forward.
        """
        Rest().bot_action_move(self.bot_id, state)

    def turn(self, direction):
        """
        Start or stop turning the bot in one direction.
        """
        Rest().bot_action_turn(self.bot_id, direction)

    def shoot(self, angle):
        """
        Shoot at the desired angle.
        """
        Rest().bot_action_shoot(self.bot_id, angle)
