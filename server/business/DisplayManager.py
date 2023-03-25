import starlette.datastructures
import websockets.connection
from fastapi import WebSocket
from business.interfaces.IDisplayManager import IDisplayManager
from business.displays.DisplayClient import DisplayClient


class DisplayManager(IDisplayManager):

    _DISPLAY_CLIENTS: dict[str, DisplayClient] = dict()

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

    def create_client(self, websocket: WebSocket, websocket_headers: starlette.datastructures.Headers,
                      host: str, port: int) -> DisplayClient:
        client = DisplayClient(display_manager=self, websocket=websocket, websocket_headers=websocket_headers,
                               id_num=len(self._DISPLAY_CLIENTS.keys()) + 1, host=host, port=port)
        self._DISPLAY_CLIENTS[client.login_id] = client
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

    def get_clients(self) -> (DisplayClient,):
        return tuple(self._DISPLAY_CLIENTS.values())

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

    async def disconnect_all_clients(self):
        for client in self._DISPLAY_CLIENTS.values():
            await client.disconnect()

    async def reset(self):
        await self.disconnect_all_clients()
        self._DISPLAY_CLIENTS.clear()
