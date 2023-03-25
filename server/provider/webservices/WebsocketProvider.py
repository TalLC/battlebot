import asyncio
import logging
from queue import SimpleQueue
from fastapi import FastAPI, WebSocket
from starlette import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from business.GameManager import GameManager
from consumer.webservices.messages.websocket.DisplayClientLoginMessage import DisplayClientLoginMessage
from consumer.webservices.messages.websocket.MapCreateMessage import MapCreateMessage
from consumer.webservices.messages.websocket.BotCreateMessage import BotCreateMessage
from consumer.webservices.messages.websocket.GameInfoMessage import GameInfoMessage
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
                websocket=websocket, websocket_headers=websocket.headers,
                host=websocket.client.host, port=websocket.client.port
            )
            logging.debug(f"[WEBSOCKET] Display {display_client.name} connected")

            # Sending game information
            logging.debug(f"[WEBSOCKET] Sending game information to {display_client.name}")
            game_info_message = GameInfoMessage(
                is_debug=GameManager().is_debug, map_id=GameManager().map.id,
                max_players=GameManager().max_players
            )
            await websocket.send_json(game_info_message.json())

            # Sending map information
            logging.debug(f"[WEBSOCKET] Sending map to {display_client.name}")
            current_map = GameManager().map
            map_create_message = MapCreateMessage(
                map_id=current_map.id, height=current_map.height,
                width=current_map.width, tiles_grid=current_map.tiles_grid
            )
            await websocket.send_json(map_create_message.json())

            # Waiting for all the bots to be ready
            while not GameManager().are_bots_ready:
                # Waiting for bots to connect
                await asyncio.sleep(1)

            # Sending all bots to webservice
            logging.debug(f"[WEBSOCKET] Sending bots to {display_client.name}")
            for bot in GameManager().bot_manager.get_bots():
                await websocket.send_json(BotCreateMessage(bot).json())

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
            logging.debug(f"[WEBSOCKET] Display {display_client.name} disconnected")

            # Removing the queue to avoid receiving messages
            self.__webservices.remove_ws_queue(client_queue)
