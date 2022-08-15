import logging
import json
from fastapi import FastAPI, HTTPException
from common.Singleton import SingletonABCMeta
from business.GameManager import GameManager


class RestAPI(metaclass=SingletonABCMeta):

    def __init__(self):
        self.app = None

    def run(self):
        self.app: FastAPI = FastAPI()
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
        @self.app.get("/")
        async def root():
            return {"status": "ok", "message": "Hello from FastAPI"}

    def __endpoint_registration(self):
        @self.app.post("/registration")
        async def registration(team_id: str, bot_name: str, bot_type: str = "warrior"):
            bot_type = bot_type.lower()

            if not GameManager().does_team_exists(team_id):
                raise HTTPException(status_code=500, detail="Unknown team")

            bot = GameManager().add_bot(team_id, bot_name, bot_type)
            if bot is None:
                raise HTTPException(status_code=500, detail="Team is full")

            return {"status": "ok", "message": "The bot has been successfully registered", "bot_id": bot.id}

    def __endpoint_request_connection(self):
        @self.app.post("/request_connection")
        async def request_connection(bot_id: str):
            from provider.ProviderManager import ProviderManager

            logging.info(f"Bot {bot_id} is requesting a connection")

            # Does bot exists
            if not GameManager().does_bot_exists(bot_id):
                raise HTTPException(status_code=500, detail="Unknown bot")

            bot = GameManager().get_bot(bot_id)
            # 3 éléments au total doivent être envoyés au client et retournés via l'endpoint "check_connection" :
            # - request_id : identifiant pour cette demande de connexion
            # - stomp_id : identifiant pour le STOMP
            # - mqtt_id : identifiant pour le MQTT

            ProviderManager().mqtt().send_message(
                "BATTLEBOT/BOT/" + bot.id,
                json.dumps({"mqtt_id": bot.client_connection.source_mqtt_id}),
                True
            )
            ProviderManager().stomp().send_message(
                "BATTLEBOT.BOT." + bot.id,
                json.dumps({"stomp_id": bot.client_connection.source_stomp_id})
            )

            return {
                "status": "ok",
                "message": "Messages sent from STOMP and MQTT",
                "request_id": bot.client_connection.source_request_id
            }

    def __endpoint_check_connection(self):
        @self.app.post("/check_connection")
        async def check_connection(bot_id, request_id: str, stomp_id: str, mqtt_id: str):
            # Does bot exists
            if not GameManager().does_bot_exists(bot_id):
                raise HTTPException(status_code=500, detail="Unknown bot")

            bot = GameManager().get_bot(bot_id)
            if bot.client_connection.source_request_id != request_id:
                raise HTTPException(status_code=500, detail="Invalid request ID")

            if bot.client_connection.source_stomp_id != stomp_id:
                raise HTTPException(status_code=500, detail="Invalid STOMP ID")

            if bot.client_connection.source_mqtt_id != mqtt_id:
                raise HTTPException(status_code=500, detail="Invalid MQTT ID")

            return {"status": "ok", "message": "Your bot is successfully connected"}

    def __endpoint_move(self):
        @self.app.post("/move")
        async def move():
            return {"status": "ok", "message": "Bot is starting to move"}

    def __endpoint_turn(self):
        @self.app.post("/turn")
        async def turn(direction: str):
            if direction.lower() in ["left", "right"]:
                return {"status": "ok", "message": f"Bot is starting to turn {direction}"}

    def __endpoint_fire(self):
        @self.app.post("/fire")
        async def fire(angle: float):
            return {"status": "ok", "message": f"Fired at {angle}°"}
