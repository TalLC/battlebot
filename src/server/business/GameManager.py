from __future__ import annotations
import logging
from time import sleep
from threading import Thread, Event
from typing import TYPE_CHECKING, Tuple, List, Union

from common.config import CONFIG_GAME
from common.Singleton import SingletonABCMeta
from business.interfaces.IGameManager import IGameManager
from business.TeamManager import TeamManager
from business.BotManager import BotManager
from business.DisplayManager import DisplayManager
from business.Map import Map
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.stomp.GameStatusMessage import GameStatusMessage

if TYPE_CHECKING:
    from business.gameobjects.entity.bots.models.BotModel import BotModel
    from business.gameobjects.tiles.Tile import Tile
    from business.gameobjects.tiles.objects.TileObject import TileObject


class GameManager(IGameManager, metaclass=SingletonABCMeta):

    @property
    def is_client_ready(self) -> bool:
        return self._is_client_ready

    @property
    def are_bots_ready(self) -> bool:
        return self._are_bots_ready

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
        self._is_client_ready = False
        self._are_bots_ready = False
        self._is_started = False
        self._max_players = CONFIG_GAME.max_players
        self.team_manager = TeamManager(self)
        self.bot_manager = BotManager(self)
        self.display_manager = DisplayManager(self)
        self.map = None
        self.load_map(CONFIG_GAME.map_id)

        # Thread auto starting the game when enough bot are connected
        self._event_stop_checking_starting_conditions = Event()
        self._thread_game_start_conditions = Thread(
            target=self._thread_check_starting_conditions,
            args=(self._event_stop_checking_starting_conditions,)
        ).start()

        # Thread to stop the game on winning conditions
        # Must be started manually when the game starts
        self._event_stop_checking_stopping_conditions = Event()
        self._thread_game_stop_conditions = Thread(
            target=self._thread_check_stopping_conditions,
            args=(self._event_stop_checking_stopping_conditions,)
        )

    def load_map(self, map_id: str):
        """
        Loads a new map.
        """
        if self.map:
            del self.map

        self.map = Map(self, map_id)

    def stop_threads(self):
        """
        Stop all the GameManager's threads.
        """
        # Set the events to stop the threads
        self._event_stop_checking_starting_conditions.set()
        self._event_stop_checking_stopping_conditions.set()

    def _wait_for_players(self, e: Event):
        """
        Thread blocking operation. Waiting until all players are connected or until the event is triggered.
        """
        current_players_count = self.registered_players_count
        while current_players_count < self._max_players and not e.is_set():
            # Check if a new player has been connected
            __tmp_p_count = self.registered_players_count

            if __tmp_p_count != current_players_count:
                # Announcing new player
                current_players_count = __tmp_p_count
                connected_bots_names = '\n'.join(
                    [f'{bot.team.name} : "{bot.name}"' for bot in self.bot_manager.get_bots()]
                )
                logging.debug(f"{current_players_count}/{self._max_players} players connected:"
                              f"\n{connected_bots_names}")
            else:
                sleep(1)

    def _wait_for_display_clients(self, e: Event):
        """
        Thread blocking operation. Waiting until at least one display client is connected.
        """
        while not self._is_client_ready and not e.is_set():
            # Check if a client is ready
            for client in self.display_manager.get_clients():
                if client.is_ready:
                    self._is_client_ready = True
                    break
            sleep(1)

    def _thread_check_starting_conditions(self, e: Event):
        """
        Thread waiting for:
         - all players to register their bots
         - at least one display client to be connected
        """
        # Waiting until all players are connected
        logging.debug("Waiting for bots to join the game...")
        self._wait_for_players(e)

        # Check if the thread is aborting
        if not e.is_set():
            # All bots are connected
            self._are_bots_ready = True
        else:
            logging.debug("Auto game start has been aborted")
            return

        # Waiting until at least one client display is connected
        logging.debug("Waiting for a display client...")
        self._wait_for_display_clients(e)

        # Start the game only if it wasn't already started from API
        if not e.is_set():
            logging.debug("Starting the game")
            self.start_game()
        else:
            logging.debug("Auto game start has been aborted")
            return

    def _thread_check_stopping_conditions(self, e: Event):
        """
        Thread waiting for:
         - one team is left alive
        """
        # Waiting until there is only one team left alive
        logging.debug("Waiting for the game to finish")
        while self.team_manager.bot_count(alive_only=True) >= 2 and not e.is_set():
            sleep(1)

        if not e.is_set():
            self.stop_game()
            logging.debug("Game is finished")
        else:
            logging.debug("Game has been aborted")

    def start_game(self):
        """
        Set the boolean to "started".
        """
        # Ensure the thread is stopped if we started the game from API
        self._event_stop_checking_starting_conditions.set()

        self._is_started = True
        logging.info(f"Game has been started with {self.registered_players_count} players!")

        # Dispatching starting message to all connected bots
        for bot in self.bot_manager.get_bots():
            ConsumerManager().stomp.send_message(GameStatusMessage(bot_id=bot.id, is_started=True))

        # Starting to check end game conditions
        self._thread_game_stop_conditions.start()

    def stop_game(self):
        """
        Stops the game.
        """
        # Ensure the thread is stopped if we have aborted the game
        self._event_stop_checking_stopping_conditions.set()
        self._is_started = False

        # Dispatching starting message to all connected bots
        for bot in self.bot_manager.get_bots():
            bot.stop()
            ConsumerManager().stomp.send_message(GameStatusMessage(bot_id=bot.id, is_started=False))

    def get_items_on_map(self, bots_only: bool = True, objects_only: bool = True, collision_only: bool = True,
                         radius: int = 0, origin: Tuple[float, float] = (0, 0)
                         ) -> Union[List[Tile], List[TileObject], List[BotModel]]:
        """
            Return items from map. Parameters define what should be returned.
        """
        entities = list()

        if radius == 0:
            # All map
            if objects_only:
                # return TileObject
                entities += self.map.tiles_grid.get_all_tiles_objects(collision_only=collision_only)
            else:
                # return Tile
                entities += self.map.tiles_grid.get_all_tiles()
        else:
            # Part of map
            if objects_only:
                # return TileObject
                entities += self.map.tiles_grid.get_tiles_objects_in_radius(collision_only=collision_only,
                                                                            origin=origin, radius=radius)
            else:
                # return Tile
                entities += self.map.tiles_grid.get_tiles_in_radius(origin=origin, radius=radius)

        if bots_only:
            # Add bots to the list
            entities += list(self.bot_manager.get_bots(connected_only=True))

        return entities
