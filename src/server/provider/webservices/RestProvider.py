import logging
from fastapi import FastAPI
from common.ErrorCode import *
from business.GameManager import GameManager
from consumer.ConsumerManager import ConsumerManager
from consumer.brokers.messages.mqtt.MQTTLoginMessage import MQTTLoginMessage
from consumer.brokers.messages.stomp.STOMPLoginMessage import STOMPLoginMessage
from provider.webservices.rest.models.AdminBaseModel import AdminBaseModel
from provider.webservices.rest.models.AdminDisplayClientsActionListModel import AdminDisplayClientsActionListModel
from provider.webservices.rest.models.AdminDisplayClientsActionGetByIdModel import AdminDisplayClientsActionGetByIdModel
from provider.webservices.rest.models.AdminDisplayClientsActionGetByTokenModel import AdminDisplayClientsActionGetByTokenModel
from provider.webservices.rest.models.DisplayClientsActionReadyModel import DisplayClientsActionReadyModel
from provider.webservices.rest.models.BotsActionRegisterModel import BotsActionRegisterModel
from provider.webservices.rest.models.BotsIdActionCheckConnectionModel import BotsIdActionCheckConnectionModel
from provider.webservices.rest.models.BotsIdActionShootModel import BotsIdActionShootModel
from provider.webservices.rest.models.BotsIdActionTurnModel import BotsIdActionTurnModel
from provider.webservices.rest.models.BotsIdActionMoveModel import BotsIdActionMoveModel
from provider.webservices.rest.models.BotsIdActionShieldRaiseModel import BotsIdActionShieldRaiseModel


class RestProvider:

    def __init__(self, app: FastAPI, admin_password: str):
        self.__app = app
        self.__register_endpoints()
        self.__admin_password = admin_password

    def __register_endpoints(self):
        self.__admin_game_action_start()
        self.__admin_display_clients_action_list()
        self.__admin_display_clients_action_get_by_id()
        self.__admin_display_clients_action_get_by_token()
        self.__display_action_ready()
        self.__bots_action_register()
        self.__bots_id_action_request_connection()
        self.__bots_id_action_check_connection()
        self.__bots_id_action_shoot()
        self.__bots_id_action_turn()
        self.__bots_id_action_move()
        self.__bots_id_action_shield_raise()
        logging.info("All endpoints registered")

    def __admin_game_action_start(self):
        """
        Start the current game.
        """
        @self.__app.patch("/game/action/start")
        async def action(model: AdminBaseModel):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            pass

    def __display_action_ready(self):
        """
        Set the display client to ready if the tokens matches.
        !!Do not use "client_token" as Path parameter to avoid clients to set ready for others!!
        """
        @self.__app.patch("/display/clients/action/ready")
        async def action(model: DisplayClientsActionReadyModel):
            # Checking if the token exists
            if not GameManager().display_manager.does_client_token_exists(model.client_token):
                ErrorCode.throw(DISPLAY_CLIENT_ID_DOES_NOT_EXISTS)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_token(model.client_token)

            # Setting client to Ready
            client.set_ready()

    def __admin_display_clients_action_list(self):
        """
        List all present and past display clients.
        """
        @self.__app.get("/display/clients/action/list")
        async def action(model: AdminDisplayClientsActionListModel):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Fetching clients information
            if model.connected_only:
                clients = GameManager().display_manager.get_connected_clients_jsons()
            else:
                clients = GameManager().display_manager.get_all_clients_jsons()

            return {'status': 'ok', 'clients': clients}

    def __admin_display_clients_action_get_by_id(self):
        """
        Find a display client by its id.
        """
        @self.__app.get("/display/clients/action/get_by_id")
        async def action(model: AdminDisplayClientsActionGetByIdModel):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Does display client exists
            if not GameManager().display_manager.does_client_id_exists(model.client_id):
                ErrorCode.throw(DISPLAY_CLIENT_ID_DOES_NOT_EXISTS)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_id(model.client_id)

            return {'status': 'ok', 'client': client.json()}

    def __admin_display_clients_action_get_by_token(self):
        """
        Find a display client by its token.
        """
        @self.__app.get("/display/clients/action/get_by_token")
        async def action(model: AdminDisplayClientsActionGetByTokenModel):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Does display client exists
            if not GameManager().display_manager.does_client_token_exists(model.client_token):
                ErrorCode.throw(DISPLAY_BAD_TOKEN)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_token(model.client_token)

            return {'status': 'ok', 'client': client.json()}

    def __bots_action_register(self):
        """
        Create a new bot object and adds it to the specified team.
        """
        @self.__app.post("/bots/action/register")
        async def action(model: BotsActionRegisterModel):
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

    def __bots_id_action_request_connection(self):
        """
        Request connection ids to validate the connection to all the services.
        It sends 3 ids to the client using Rest, STOMP and MQTT.
        The client must send back these ids to the server to validate the connection.
        """
        @self.__app.get("/bots/{bot_id}/action/request_connection")
        async def action(bot_id: str):
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

    def __bots_id_action_check_connection(self):
        """
        Check if the ids found by the client are the expected ones in order to validate the client connection to all
        our services.
        """
        @self.__app.patch("/bots/{bot_id}/action/check_connection")
        async def action(bot_id: str, model: BotsIdActionCheckConnectionModel):
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

    def __bots_id_action_shoot(self):
        """
        Make the bot shoot to the desired relative angle.
        """
        @self.__app.patch("/bots/{bot_id}/action/shoot")
        async def action(bot_id: str, model: BotsIdActionShootModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            return {"status": "ok", "message": f"Fired at {model.angle}°"}

    def __bots_id_action_turn(self):
        """
        Start to turn the specified bot to its left or right.
        """
        @self.__app.patch("/bots/{bot_id}/action/turn")
        async def action(bot_id: str, model: BotsIdActionTurnModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            if model.direction.lower() in ["left", "right"]:
                return {"status": "ok", "message": f"Bot is starting to turn {model.direction}"}
            elif model.direction.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped turning"}

    def __bots_id_action_move(self):
        """
        Start to move the specified bot forward.
        """
        @self.__app.patch("/bots/{bot_id}/action/move")
        async def action(bot_id: str, model: BotsIdActionMoveModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            if model.action.lower() == 'start':
                return {"status": "ok", "message": "Bot is starting to move"}
            elif model.action.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped moving"}

    def __bots_id_action_shield_raise(self):
        """
        Raise or lower the shield of the specified bot.
        """
        @self.__app.patch("/bots/{bot_id}/action/shield_raise")
        async def action(bot_id: str, model: BotsIdActionShieldRaiseModel):
            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            if model.action.lower() == 'start':
                return {"status": "ok", "message": "Bot is starting to use its shield."}
            elif model.action.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped to use its shield."}
