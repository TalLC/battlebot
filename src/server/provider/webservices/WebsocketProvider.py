import asyncio
import logging
from queue import SimpleQueue
from fastapi import FastAPI, WebSocket
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from business.GameManager import GameManager
from consumer.webservices.messages.websocket.models.DisplayClientLoginMessage import DisplayClientLoginMessage
from consumer.webservices.messages.websocket.MapCreateMessage import MapCreateMessage
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

            # Websocket message queue
            client_queue = SimpleQueue()
            self.__webservices.add_ws_queue(client_queue)

            # Creating a Display Client object to log websocket connection
            display_client = GameManager().display_manager.create_client(
                host=websocket.client.host, port=websocket.client.port, websocket_headers=websocket.headers
            )
            logging.debug(f"Display {display_client.name} connected")

            # Todo: déporter la création de map pour permettre la modification de la map avant le début de partie
            logging.debug(f"Sending map to {display_client.name}")

            # Sending map information
            current_map = GameManager().map
            map_create_message = MapCreateMessage(map_id=current_map.id, height=current_map.height,
                                                  width=current_map.width, tiles_grid=current_map.tiles_grid)
            await websocket.send_json(map_create_message.json())

            # Waiting for all the bots to be ready
            while not GameManager().are_bots_ready:

                # Waiting for bots to connect
                await asyncio.sleep(1)

            # Sending all bots to webservice
            for bot in GameManager().bot_manager.get_bots():
                await websocket.send_json(BotCreateMessage(bot_id=bot.id, x=bot.x, z=bot.z, ry=bot.ry).json())

            # Sending token to the client in order to send it back using Rest when ready
            await websocket.send_json(DisplayClientLoginMessage(display_client).json())

            # While client is connected, we send them the messages
            while websocket.client_state == websockets.WebSocketState.CONNECTED:
                try:
                    # While we have messages in the queue
                    while not client_queue.empty():
                        # Reading message
                        data_send = client_queue.get()
                        logging.debug(f"[WEBSOCKET] Sending message: {data_send}")

                        # Sending message to display
                        await websocket.send_json(data_send)

                    # No messages, waiting
                    await asyncio.sleep(0.1)
                except ConnectionClosedOK:
                    # Client has closed the connection
                    break
                except ConnectionClosedError:
                    # Connection has closed due to an error
                    break

            # Disconnecting the display
            display_client.set_connection_closed()
            logging.debug(f"Display {display_client.name} disconnected")

            # Removing the queue to avoid receiving messages
            self.__webservices.remove_ws_queue(client_queue)
