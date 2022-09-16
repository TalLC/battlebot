import logging
from fastapi import FastAPI, HTTPException
from business.GameManager import GameManager
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.mqtt.MQTTLoginMessage import MQTTLoginMessage
from consumer.brokers.messages.stomp.STOMPLoginMessage import STOMPLoginMessage


class RestProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_endpoints()

    def __register_endpoints(self):
        self.__endpoint_root()
        self.__endpoint_registration()
        self.__endpoint_request_connection()
        self.__endpoint_check_connection()
        self.__endpoint_move()
        self.__endpoint_turn()
        self.__endpoint_fire()
        logging.info("All endpoints registered")

    def __endpoint_root(self):
        @self.__app.get("/")
        async def root():
            return {"status": "ok", "message": "Hello from FastAPI"}

    def __endpoint_registration(self):
        @self.__app.post("/registration")
        async def registration(team_id: str, bot_name: str, bot_type: str = "warrior"):
            bot_type = bot_type.lower()

            if not GameManager().team_manager.does_team_exists(team_id):
                raise HTTPException(status_code=500, detail="Unknown team")

            bot = GameManager().bot_manager.create_bot(bot_name, bot_type)
            is_bot_added = GameManager().team_manager.get_team(team_id).add_bot(bot)
            if not is_bot_added:
                raise HTTPException(status_code=500, detail="Team is full")

            return {"status": "ok", "message": "The bot has been successfully registered", "bot_id": bot.id}

    def __endpoint_request_connection(self):
        """
        Request connection ids to validate the connection to all the services.
        It sends 3 ids to the client using Rest, STOMP and MQTT.
        The client must send back these ids to the server to validate the connection.
        """
        @self.__app.post("/request_connection")
        async def request_connection(bot_id: str):
            logging.info(f"Bot {bot_id} is requesting a connection")

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                raise HTTPException(status_code=500, detail="Unknown bot")

            bot = GameManager().bot_manager.get_bot(bot_id)

            # Sending 3 different ids to the client using 3 different channels
            # Rest, STOMP and MQTT
            ConsumerManager().mqtt.send_message(MQTTLoginMessage(bot.id, bot.client_connection.source_mqtt_id))
            ConsumerManager().stomp.send_message(STOMPLoginMessage(bot.id, bot.client_connection.source_stomp_id))

            return {
                "status": "ok",
                "message": "Messages sent from STOMP and MQTT",
                "request_id": bot.client_connection.source_request_id
            }

    def __endpoint_check_connection(self):
        @self.__app.post("/check_connection")
        async def check_connection(bot_id, request_id: str, stomp_id: str, mqtt_id: str):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                raise HTTPException(status_code=500, detail="Unknown bot")

            bot = GameManager().bot_manager.get_bot(bot_id)
            if bot.client_connection.source_request_id != request_id:
                raise HTTPException(status_code=500, detail="Invalid request ID")

            if bot.client_connection.source_stomp_id != stomp_id:
                raise HTTPException(status_code=500, detail="Invalid STOMP ID")

            if bot.client_connection.source_mqtt_id != mqtt_id:
                raise HTTPException(status_code=500, detail="Invalid MQTT ID")

            return {"status": "ok", "message": "Your bot is successfully connected"}

    def __endpoint_move(self):
        @self.__app.post("/move")
        async def move():
            return {"status": "ok", "message": "Bot is starting to move"}

    def __endpoint_turn(self):
        @self.__app.post("/turn")
        async def turn(direction: str):
            if direction.lower() in ["left", "right"]:
                return {"status": "ok", "message": f"Bot is starting to turn {direction}"}

    def __endpoint_fire(self):
        @self.__app.post("/fire")
        async def fire(angle: float):
            return {"status": "ok", "message": f"Fired at {angle}°"}