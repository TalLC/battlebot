import starlette.datastructures
from business.interfaces.IDisplayManager import IDisplayManager
from business.displays.DisplayClient import DisplayClient


class DisplayManager(IDisplayManager):
    _DISPLAY_CLIENTS = dict()

    def does_client_id_exists(self, id_num: int):
        """
        Check if a display client exists.
        """
        for client in self._DISPLAY_CLIENTS.values():
            if client.id == id_num:
                return True
        return False

    def does_client_token_exists(self, token: str):
        """
        Check if a display client exists.
        """
        if token in self._DISPLAY_CLIENTS.keys():
            return True
        return False

    def create_client(self, host: str, port: int, websocket_headers: starlette.datastructures.Headers) -> DisplayClient:
        client = DisplayClient(len(self._DISPLAY_CLIENTS.keys()) + 1, host, port, websocket_headers)
        self._DISPLAY_CLIENTS[client.token] = client
        return client

    def get_client_by_token(self, token: str) -> None | DisplayClient:
        if token in self._DISPLAY_CLIENTS.keys():
            return self._DISPLAY_CLIENTS[token]
        else:
            return None

    def get_client_by_id(self, id_num: int) -> None | DisplayClient:
        for client in self._DISPLAY_CLIENTS.values():
            if client.id == id_num:
                return client
        return None

    def get_clients(self) -> [DisplayClient]:
        return list(self._DISPLAY_CLIENTS.values())

    def get_all_clients_jsons(self) -> list:
        data = list()
        for client in self._DISPLAY_CLIENTS.values():
            data.append(client.json())
        return data

    def get_connected_clients_jsons(self) -> list:
        data = list()
        for client in self._DISPLAY_CLIENTS.values():
            if client.status == 'connected':
                data.append(client.json())
        return data
