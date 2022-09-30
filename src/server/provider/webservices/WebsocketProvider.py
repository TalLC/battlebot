import asyncio
import logging
from queue import SimpleQueue
from fastapi import FastAPI, WebSocket
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from business.GameManager import GameManager
from consumer.webservices.messages.websocket.models.MapCreateMessage import MapCreateMessage
from consumer.webservices.messages.websocket.models.MapUpdateMessage import MapUpdateMessage
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

            # while not GameManager().map.is_ready:
            #     await asyncio.sleep(1)

            # Todo: déporter la création de map pour permettre la modification de la map avant le début de partie
            logging.debug(f"Sending map to {display_client.name}")

            # Sending map information
            current_map = GameManager().map
            map_create_message = MapCreateMessage(map_id=current_map.id, height=current_map.height,
                                                  width=current_map.width, tiles=current_map.tiles)
            await websocket.send_json(map_create_message.json())

            # Keeping a track of which bots were sent
            sent_bot = list()

            # Waiting for the display to be ready and the game to start
            while not display_client.is_ready and not GameManager().is_started:

                # Sending bots information as they connect
                for bot in GameManager().bot_manager.get_bots():

                    # A new bot is connected
                    if bot.id not in sent_bot and bot.client_connection.is_connected:
                        await websocket.send_json(BotCreateMessage(bot_id=bot.id, x=bot.x, z=bot.z, ry=bot.ry))
                        sent_bot.append(bot.id)

                # Waiting for bots to connect
                await asyncio.sleep(1)

            # While client is connected, we send them the messages
            while websocket.client_state == websockets.WebSocketState.CONNECTED:
                try:
                    # While we have messages in the queue
                    while not client_queue.empty():
                        # Reading message
                        data_send = client_queue.get()
                        logging.debug(f"[WEBSOCKET] Sending '{data_send.msg_type}' message: {data_send.json()}")

                        # Sending message to display
                        await websocket.send_json(data_send.json())

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

            # Removing the queue to avoir receiving messages
            self.__webservices.remove_ws_queue(client_queue)
