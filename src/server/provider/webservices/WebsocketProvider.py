import logging
import asyncio
from queue import SimpleQueue
from fastapi import FastAPI, WebSocket
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK
from business.GameManager import GameManager
from utils.webservices import Webservices
import time


class WebsocketProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__webservices = Webservices()
        self.__register_websocket()

    def __register_websocket(self):
        @self.__app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            queue = SimpleQueue()
            self.__webservices.add_ws_queue(queue)
            data_send = {}

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
                    await websocket.send_json(data_send)
                    # await asyncio.sleep(1)
                except ConnectionClosedOK:
                    break

            self.__webservices.remove_ws_queue(queue)
