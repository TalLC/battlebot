import logging
from business.GameManager import GameManager
from fastapi import FastAPI, HTTPException


class RestAPI:

    def __init__(self):
        self.app = None

    def run(self):
        self.app: FastAPI = FastAPI()
        self.__register_endpoints()

    def __register_endpoints(self):
        self.__endpoint_root()
        self.__endpoint_registration()
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

            bot_id = GameManager().register_bot(team_id, bot_name, bot_type)
            if bot_id is None or bot_id == str():
                raise HTTPException(status_code=500, detail="Team is full")

            return {"status": "ok", "message": "The bot has been successfully registered", "bot_id": bot_id}

    def __endpoint_check_connections(self):
        @self.app.post("/check_connections")
        async def check_connections(bot_id: str):

            # Check si robot existe

            # MAJ les id de connectivité attendus par le robot

            # Envoyer un message sur STOMP et MQTT à récupérer par le client
            # Envoyer l'ID STOMP et MQTT que le client devra lire dans les messages
            return {"status": "ok", "message": "Messages sent from STOMP and MQTT", "stomp_id": "123", "mqtt_id": "456"}

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
