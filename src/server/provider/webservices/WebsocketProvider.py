import asyncio
from queue import SimpleQueue
from fastapi import FastAPI, WebSocket
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from business.GameManager import GameManager
from consumer.webservices.messages.websocket.BotCreateMessage import BotCreateMessage
from provider.security.NetworkSecurityDecorators import NetworkSecurityDecorators
from utils.webservices import Webservices


class WebsocketProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__webservices = Webservices()
        self.__register_websocket()

    def __register_websocket(self):

        @self.__app.websocket("/ws")
        @NetworkSecurityDecorators.websocket_ban_check
        @NetworkSecurityDecorators.websocket_autoban
        async def websocket_endpoint(websocket: WebSocket):
            client_queue = SimpleQueue()
            self.__webservices.add_ws_queue(client_queue)

            display_client = GameManager().display_manager.create_client(host=websocket.client.host,
                                                                         port=websocket.client.port,
                                                                         websocket_headers=websocket.headers)
            print(display_client)

            # while not GameManager().map.is_ready:
            #     await asyncio.sleep(1)

            await websocket.send_json(GameManager().map.data)
            sent_bot = list()
            while not display_client.is_ready and not GameManager().is_started:
                await asyncio.sleep(1)
                for bot in GameManager().bot_manager.get_bots():
                    if bot.id not in sent_bot and bot.client_connection.is_connected:
                        await websocket.send_json(BotCreateMessage(bot_id=bot.id, x=bot.x, z=bot.z, ry=bot.ry))
                        sent_bot.append(bot.id)

            # While client is connected, we send them the messages
            while websocket.client_state == websockets.WebSocketState.CONNECTED:
                try:
                    while not client_queue.empty():
                        data_send = client_queue.get()
                        await websocket.send_json(data_send.json())
                    await asyncio.sleep(0.1)
                except ConnectionClosedOK:
                    break
                except ConnectionClosedError:
                    break

            display_client.set_connection_closed()
            print(display_client)

            self.__webservices.remove_ws_queue(client_queue)
