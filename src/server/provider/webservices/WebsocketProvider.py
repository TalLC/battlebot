import asyncio
from queue import SimpleQueue

from fastapi import FastAPI, WebSocket
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from business.GameManager import GameManager
from utils.webservices import Webservices
import time

from provider.security.decorators import antispam_websocket


class WebsocketProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__webservices = Webservices()
        self.__register_websocket()

    def __register_websocket(self):

        @self.__app.websocket("/ws")
        @antispam_websocket
        async def websocket_endpoint(websocket: WebSocket):
            queue = SimpleQueue()
            self.__webservices.add_ws_queue(queue)
            data_send = {}

            display_client = GameManager().display_manager.create_client(
                host=websocket.client.host, port=websocket.client.port, websocket_headers=websocket.headers
            )
            print(display_client)

            # while !GameManager().map.is_ready:
            #     await asyncio.sleep(1)
            #
            # await webservices.send_json(GameManager().map.data)
            #
            # while !GameManager().is_game_started:
            #     await asyncio.sleep(1)

            # While client is connected, we send them the messages
            while websocket.client_state == websockets.WebSocketState.CONNECTED:
                try:
                    timer = time.time()
                    while time.time() - timer > 100:
                        data = queue.get()
                        data_send[data.pop('name')] = data
                    await websocket.send_json(data_send)
                    await asyncio.sleep(1)
                except ConnectionClosedOK:
                    break
                except ConnectionClosedError:
                    break

            display_client.set_connection_closed()
            print(display_client)

            self.__webservices.remove_ws_queue(queue)
