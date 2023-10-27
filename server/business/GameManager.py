from __future__ import annotations
import logging
from time import sleep
from threading import Thread, Event
from typing import TYPE_CHECKING, Tuple
from common.Singleton import SingletonABCMeta
from enum import Enum

from business.MapManager import MapManager
from common.PerformanceCounter import PerformanceCounter
from business.interfaces.IGameManager import IGameManager
from business.TeamManager import TeamManager
from business.BotManager import BotManager
from business.DisplayManager import DisplayManager
from business.maps.Map import Map
from consumer.ConsumerManager import ConsumerManager
from consumer.webservices.messages.websocket.GameEndMessage import GameEndMessage
from consumer.brokers.messages.stomp.GameStatusMessage import GameStatusMessage
from business.PluginManager import PluginManager

if TYPE_CHECKING:
    from business.gameobjects.GameObject import GameObject
    from business.interfaces.IPluginSpawn import IPluginSpawn


class GameStatus(Enum):
    NOT_INITIALIZED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3
    STOPPED = 4


class GameManager(IGameManager, metaclass=SingletonABCMeta):

    @property
    def is_debug(self) -> bool:
        return self._is_debug

    @property
    def plugins_spawn(self) -> IPluginSpawn:
        return self._plugins_spawn

    @property
    def is_client_ready(self) -> bool:
        return self._is_client_ready

    @property
    def are_bots_ready(self) -> bool:
        return self._are_bots_ready

    @property
    def is_started(self) -> bool:
        return self._status == GameStatus.STARTED

    @property
    def is_starting(self) -> bool:
        return self._status == GameStatus.STARTING

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def is_full(self) -> bool:
        return self.registered_players_count >= self.max_players

    @property
    def game_map(self) -> Map:
        return self._game_map

    @property
    def max_players(self) -> int:
        return self._max_players

    @property
    def registered_players_count(self) -> int:
        return self.bot_manager.get_bots_count()

    def __init__(self):
        self._is_client_ready = False
        self._are_bots_ready = False
        self._status = GameStatus.NOT_INITIALIZED
        self.team_manager = TeamManager(self)
        self.bot_manager = BotManager(self)
        self.map_manager = MapManager(self)
        self.display_manager = DisplayManager(self)

        # Loading config
        self._is_debug = False
        self._max_players = 0
        self._game_map = None
        self._plugins_spawn: IPluginSpawn | None = None
        self.load_config()

        # Thread auto starting the game when enough bot are connected
        self._event_stop_checking_starting_conditions = Event()
        self._thread_game_start_conditions = None

        # Thread to stop the game on winning conditions
        # Must be started manually when the game starts
        self._event_stop_checking_stopping_conditions = Event()
        self._thread_game_stop_conditions = None

    def load_config(self):
        # Importing config variable here everytime we call the function in order to refresh it
        from common.config import CONFIG_GAME

        # Reloading config
        self._is_debug = CONFIG_GAME.is_debug
        self._max_players = CONFIG_GAME.max_players

    def load_map(self, map_id: str):
        """
        Loads a new map
        """
        if self._game_map:
            logging.debug(f"[GAME_MANAGER] Unloading previous map: {self._game_map.id}")
            del self._game_map

        logging.debug(f"[GAME_MANAGER] Loading new map: {map_id}")
        self._game_map = self.map_manager.get_map(map_id)
        self._plugins_spawn = PluginManager.get_plugin_spawn_for_map(self.game_map)

    def init_threads(self):
        # Reset Events
        logging.debug("[GAME_MANAGER] Resetting threads events objects")
        self._event_stop_checking_starting_conditions.clear()
        self._event_stop_checking_stopping_conditions.clear()

        # Reset Threads
        logging.debug("[GAME_MANAGER] Resetting threads")
        self._thread_game_start_conditions = Thread(
            target=self._thread_check_starting_conditions,
            args=(self._event_stop_checking_starting_conditions,)
        )
        self._thread_game_stop_conditions = Thread(
            target=self._thread_check_stopping_conditions,
            args=(self._event_stop_checking_stopping_conditions,)
        )

        logging.debug("[GAME_MANAGER] Starting thread: Check starting conditions")
        self._thread_game_start_conditions.start()

    def stop_threads(self):
        """
        Stop all the GameManager's threads
        """
        # Set the events to stop the threads
        logging.debug("[GAME_MANAGER] Stopping threads")
        self._event_stop_checking_starting_conditions.set()
        logging.debug("[GAME_MANAGER] Stopping thread: Check starting conditions")
        self._event_stop_checking_stopping_conditions.set()
        logging.debug("[GAME_MANAGER] Stopping thread: Check stopping conditions")

    def _wait_for_players(self, e: Event):
        """
        Thread blocking operation. Waiting until all players are connected or until the event is triggered
        """
        current_players_count = self.registered_players_count
        while not self.is_full and not e.is_set():
            # Check if a new player has been connected
            __tmp_p_count = self.registered_players_count

            if __tmp_p_count != current_players_count:
                # Announcing new player
                current_players_count = __tmp_p_count
                connected_bots_names = '\n'.join(
                    [f'{bot.team.id} : "{bot.name}"' for bot in self.bot_manager.get_bots()]
                )
                logging.debug(f"[GAME_MANAGER] {current_players_count}/{self._max_players} players connected:"
                              f"\n{connected_bots_names}")
            else:
                sleep(1)

    def _wait_for_display_clients(self, e: Event):
        """
        Thread blocking operation. Waiting until at least one display client is connected
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
        logging.debug("[GAME_MANAGER] Waiting for bots to join the game...")
        self._wait_for_players(e)
        for bot in self.bot_manager.get_bots():
            bot.x, bot.z, bot.ry = self.get_spawn_coordinates(bot.team.id)

        # Check if the thread is aborting
        if not e.is_set():
            # All bots are connected
            self._are_bots_ready = True
        else:
            logging.debug("[GAME_MANAGER] Auto game start has been aborted")
            self._status = GameStatus.STOPPED
            return

        # Waiting until at least one client display is connected
        logging.debug("[GAME_MANAGER] Waiting for a display client...")
        self._wait_for_display_clients(e)

        # Start the game only if it wasn't already started from API
        if not e.is_set():
            logging.debug("[GAME_MANAGER] Starting the game")
            self.start_game()
        else:
            logging.debug("[GAME_MANAGER] Auto game start has been aborted")
            self._status = GameStatus.STOPPED
            return

    def _thread_check_stopping_conditions(self, e: Event):
        """
        Thread waiting for:
         - one team is left alive
        """
        # Waiting until there is only one team left alive
        logging.debug("[GAME_MANAGER] Waiting for the game to finish")
        while self.team_manager.team_count(alive_only=True) >= 2 and not e.is_set():
            sleep(1)

        if not e.is_set():
            self.stop_game()
            logging.debug("[GAME_MANAGER] Game is finished")
            bots_alive = self.bot_manager.get_bots(connected_only=True, alive_only=True)
            winner_name = "Nobody"
            if len(bots_alive):
                winner_name = bots_alive[0].team.name
            ConsumerManager().websocket.send_message(GameEndMessage(winner_name=winner_name))
        else:
            logging.debug("[GAME_MANAGER] Game has been aborted")
            self._status = GameStatus.STOPPED

        logging.debug("[GAME_MANAGER] Removing in memory bots from bot manager")
        self.bot_manager.reset()
        logging.debug("[GAME_MANAGER] Removing in memory bots from teams and recreating teams")
        self.team_manager.reload_teams()

    def new_game(self):
        """
        Starts a new game
        """
        # Refreshing game config
        self.load_config()

        # Check if a map has been set
        if self.game_map is None:
            logging.error("No map selected!")
            return

        # Stop the current game if any
        if self._status == GameStatus.STARTED:
            logging.debug("[GAME_MANAGER] Game is already started: stopping game")
            self.stop_game()

            while self._status in [GameStatus.STARTED, GameStatus.STOPPING]:
                logging.debug("[GAME_MANAGER] Waiting for game to stop...")
                sleep(100/1000)

            logging.debug("[GAME_MANAGER] Removing in memory bots from bot manager")
            self.bot_manager.reset()
            logging.debug("[GAME_MANAGER] Removing in memory bots from teams and recreating teams")
            self.team_manager.reload_teams()

        self._status = GameStatus.STARTING
        logging.debug(f"[GAME_MANAGER] Game status: {self._status.name}")

        logging.debug("[GAME_MANAGER] Initializing threads")
        self.init_threads()

    def start_game(self):
        """
        Set the boolean to "started"
        """
        # Ensure the thread is stopped if we started the game from API
        logging.debug("[GAME_MANAGER] Stopping thread: Check starting conditions")
        self._event_stop_checking_starting_conditions.set()

        self._status = GameStatus.STARTED
        logging.info(f"Game has been started with {self.registered_players_count} players!")

        # Dispatching starting message to all connected bots
        logging.debug("[GAME_MANAGER] Dispatching starting message to all connected bots")
        for bot in self.bot_manager.get_bots():
            logging.debug(f"[GAME_MANAGER] Dispatching to bot {bot.name}")
            ConsumerManager().stomp.send_message(GameStatusMessage(bot_id=bot.id, is_started=True))

        # Starting to check end game conditions
        logging.debug("[GAME_MANAGER] Starting thread: Check stopping conditions")
        self._thread_game_stop_conditions.start()

    def stop_game(self):
        """
        Stops the game.
        """
        # Ensure the thread is stopped if we have aborted the game
        self._status = GameStatus.STOPPING
        logging.debug(f"[GAME_MANAGER] Game status: {self._status.name}")

        logging.debug("[GAME_MANAGER] Stopping thread: Check stopping conditions")
        self._event_stop_checking_stopping_conditions.set()
        self._are_bots_ready = False
        self._is_client_ready = False

        # Dispatching stop message to all connected bots
        for bot in self.bot_manager.get_bots(alive_only=True):
            logging.debug(f"[GAME_MANAGER] Stopping bot {bot.name}")
            bot.stop()
            ConsumerManager().stomp.send_message(GameStatusMessage(bot_id=bot.id, is_started=False))

        self._status = GameStatus.STOPPED
        logging.debug(f"[GAME_MANAGER] Game status: {self._status.name}")

    @PerformanceCounter.count
    def get_map_objects(self, bots: bool = True, tiles: bool = True, non_walkable_only: bool = False,
                        tile_objects: bool = True, collision_only: bool = True, radius: int = 0,
                        origin: tuple[float, float] = (0, 0)) -> list[GameObject]:
        """
        Return objects from the map. Parameters define what should be returned
        """
        game_objects = list()

        if radius <= 0:
            # All map
            if tile_objects:
                # return TileObject
                game_objects += self.game_map.tiles_grid.get_all_tiles_objects(collision_only=collision_only)
            if tiles:
                # return Tile
                game_objects += self.game_map.tiles_grid.get_all_tiles(non_walkable_only=non_walkable_only)
            if bots:
                # Add bots to the list
                game_objects += self.bot_manager.get_bots(connected_only=True)
        else:
            # Part of map
            if tile_objects:
                # return TileObject
                game_objects += self.game_map.tiles_grid.get_tiles_objects_in_radius(
                    collision_only=collision_only, origin=origin, radius=radius
                )
            if tiles:
                # return Tile
                game_objects += self.game_map.tiles_grid.get_tiles_in_radius(
                    non_walkable_only=non_walkable_only, origin=origin, radius=radius
                )
            if bots:
                # Add bots to the list
                game_objects += self.bot_manager.get_bots_in_radius(
                    connected_only=True, origin=origin, radius=radius
                )

        return game_objects

    @PerformanceCounter.count
    def get_map_object_from_id(self, object_id: str) -> GameObject | None:
        """
        Return the game object corresponding to the specified id
        """
        for game_object in self.get_map_objects(bots=True, tiles=True, tile_objects=True, collision_only=False):
            if game_object.id == object_id:
                return game_object
        return None

    def get_spawn_coordinates(self, team_id) -> Tuple[float, float, float]:
        """
        Return spawn coordinates according to the selected plugin.
        """
        return self.plugins_spawn.process(team_id)
