from abc import ABC, abstractmethod
import starlette.datastructures
from business.displays.DisplayClient import DisplayClient


class IDisplayManager(ABC):

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
    def create_client(self, host: str, port: int, websocket_headers: starlette.datastructures.Headers) -> str:
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
