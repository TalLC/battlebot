import logging
from fastapi import FastAPI
from common.ErrorCode import *
from business.GameManager import GameManager
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.mqtt.MQTTLoginMessage import MQTTLoginMessage
from consumer.brokers.messages.stomp.STOMPLoginMessage import STOMPLoginMessage
from provider.webservices.rest.models.DisplayActionReadyModel import DisplayActionReadyModel
from provider.webservices.rest.models.BotActionRegisterModel import BotActionRegisterModel
from provider.webservices.rest.models.BotIdActionCheckConnectionModel import BotIdActionCheckConnectionModel
from provider.webservices.rest.models.BotIdActionShootModel import BotIdActionShootModel
from provider.webservices.rest.models.BotIdActionTurnModel import BotIdActionTurnModel
from provider.webservices.rest.models.BotIdActionMoveModel import BotIdActionMoveModel
from provider.webservices.rest.models.BotIdActionShieldRaiseModel import BotIdActionShieldRaiseModel


class RestProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_endpoints()

    def __register_endpoints(self):
        self.__display_action_ready()
        self.__bot_action_register()
        self.__bot_id_action_request_connection()
        self.__bot_id_action_check_connection()
        self.__bot_id_action_shoot()
        self.__bot_id_action_turn()
        self.__bot_id_action_move()
        self.__bot_id_action_shield_raise()
        logging.info("All endpoints registered")

    def __display_action_ready(self):
        @self.__app.patch("/display/action/ready")
        async def ready(model: DisplayActionReadyModel):
            pass

    def __bot_action_register(self):
        """
        Create a new bot object and adds it to the specified team.
        """
        @self.__app.post("/bot/action/register")
        async def registration(model: BotActionRegisterModel):
            bot_type = model.bot_type.lower()

            # Does team exists?
            if not GameManager().team_manager.does_team_exists(model.team_id):
                ErrorCode.throw(TEAM_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.create_bot(model.bot_name, bot_type)

            # Adding the bot to the team
            is_bot_added = GameManager().team_manager.get_team(model.team_id).add_bot(bot)
            if not is_bot_added:
                ErrorCode.throw(TEAM_IS_FULL)

            return {"status": "ok", "message": "The bot has been successfully registered", "bot_id": bot.id}

    def __bot_id_action_request_connection(self):
        """
        Request connection ids to validate the connection to all the services.
        It sends 3 ids to the client using Rest, STOMP and MQTT.
        The client must send back these ids to the server to validate the connection.
        """
        @self.__app.get("/bot/{bot_id}/action/request_connection")
        async def request_connection(bot_id: str):
            logging.info(f"Bot {bot_id} is requesting a connection")

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
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

    def __bot_id_action_check_connection(self):
        """
        Check if the ids found by the client are the expected ones in order to validate the client connection to all
        our services.
        """
        @self.__app.patch("/bot/{bot_id}/action/check_connection")
        async def check_connection(bot_id: str, model: BotIdActionCheckConnectionModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Compare request ID
            if bot.client_connection.source_request_id != model.request_id:
                ErrorCode.throw(LOGIN_INVALID_REQUEST_ID)

            # Compare STOMP ID
            if bot.client_connection.source_stomp_id != model.stomp_id:
                ErrorCode.throw(LOGIN_INVALID_STOMP_ID)

            # Compare MQTT ID
            if bot.client_connection.source_mqtt_id != model.mqtt_id:
                ErrorCode.throw(LOGIN_INVALID_MQTT_ID)

            return {"status": "ok", "message": "Your bot is successfully connected"}

    def __bot_id_action_shoot(self):
        """
        Make the bot shoot to the desired relative angle.
        """
        @self.__app.patch("/bot/{bot_id}/action/shoot")
        async def fire(bot_id: str, model: BotIdActionShootModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            return {"status": "ok", "message": f"Fired at {model.angle}°"}

    def __bot_id_action_turn(self):
        """
        Start to turn the specified bot to its left or right.
        """
        @self.__app.patch("/bot/{bot_id}/action/turn")
        async def turn(bot_id: str, model: BotIdActionTurnModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            if model.direction.lower() in ["left", "right"]:
                return {"status": "ok", "message": f"Bot is starting to turn {model.direction}"}
            elif model.direction.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped turning"}

    def __bot_id_action_move(self):
        """
        Start to move the specified bot forward.
        """
        @self.__app.patch("/bot/{bot_id}/action/move")
        async def move(bot_id: str, model: BotIdActionMoveModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            if model.action.lower() == 'start':
                return {"status": "ok", "message": "Bot is starting to move"}
            elif model.action.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped moving"}

    def __bot_id_action_shield_raise(self):
        """
        Raise or lower the shield of the specified bot.
        """
        @self.__app.patch("/bot/{bot_id}/action/shield_raise")
        async def shield_raise(bot_id: str, model: BotIdActionShieldRaiseModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            if model.action.lower() == 'start':
                return {"status": "ok", "message": "Bot is starting to use its shield."}
            elif model.action.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped to use its shield."}
