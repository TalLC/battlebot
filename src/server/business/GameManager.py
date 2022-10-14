import logging
from time import sleep
from threading import Thread, Event
from common.config import CONFIG_GAME
from common.Singleton import SingletonABCMeta
from business.interfaces.IGameManager import IGameManager
from business.TeamManager import TeamManager
from business.BotManager import BotManager
from business.DisplayManager import DisplayManager
from business.Map import Map


class GameManager(IGameManager, metaclass=SingletonABCMeta):

    @property
    def is_started(self) -> bool:
        return self._is_started

    @property
    def max_players(self) -> int:
        return self._max_players

    @property
    def registered_players_count(self) -> int:
        return self.bot_manager.get_bots_count()

    def __init__(self):
        self._is_started = False
        self._max_players = CONFIG_GAME.max_players
        self.team_manager = TeamManager(self)
        self.bot_manager = BotManager(self)
        self.display_manager = DisplayManager(self)
        self.map = Map(self, CONFIG_GAME.map_id)

        # Thread auto starting the game when enough bot are connected
        self._thread_event = Event()
        self._thread_messages = Thread(target=self._thread_check_player_count, args=(self._thread_event,)).start()

    def stop_threads(self):
        """
        Stop all threads for this bot.
        """
        # Set the event to stop the thread
        self._thread_event.set()

    def _thread_check_player_count(self, e: Event):
        """
        Thread waiting for all players to register their bots.
        """
        # Looping until all players are connected or until the thread is stopped
        current_players_count = self.registered_players_count
        while current_players_count < self._max_players and not e.is_set():

            # Check if a new player has been connected
            __tmp_p_count = self.registered_players_count
            if __tmp_p_count != current_players_count:
                current_players_count = __tmp_p_count
                connected_bots_names = ', '.join([f'"{bot.name}"' for bot in self.bot_manager.get_bots()])
                logging.debug(f"{current_players_count}/{self._max_players} players connected:"
                              f"\n{connected_bots_names}")
            else:
                sleep(1)

        # Start the game only if it wasn't already started from API
        if not e.is_set():
            self.start_game()

    def start_game(self):
        """
        Set the boolean to "started".
        """
        # Ensure the thread is stopped if we started the game from API
        self._thread_event.set()

        self._is_started = True
        logging.info(f"Game has been started with {self.registered_players_count} players!")
