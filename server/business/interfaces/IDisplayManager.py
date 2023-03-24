from __future__ import annotations
from abc import ABC, abstractmethod
from fastapi import WebSocket
import starlette.datastructures
from business.displays.DisplayClient import DisplayClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business.GameManager import GameManager


class IDisplayManager(ABC):

    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

    @abstractmethod
    def does_client_id_exists(self, id_num: int):
        """
        Check if a display client exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def does_client_token_exists(self, token: str):
        """
        Check if a display client exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_client(self, websocket: WebSocket, websocket_headers: starlette.datastructures.Headers,
                      host: str, port: int) -> str:
        """
        Create a new display client.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_client_by_token(self, token: str) -> None | DisplayClient:
        """
        Get a display client by its token.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_client_by_id(self, id_num: int) -> None | DisplayClient:
        """
        Get a display client by its id.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_clients(self) -> [DisplayClient]:
        """
        Get all display clients.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all_clients_jsons(self) -> list:
        """
        Return all clients json information.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_connected_clients_jsons(self) -> list:
        """
        Return connected  clients json information.
        """
        raise NotImplementedError()

    @abstractmethod
    def disconnect_all_clients(self):
        """
        Disconnect all clients from their websocket.
        """
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        """
        Disconnect and remove all clients.
        """
        raise NotImplementedError()
