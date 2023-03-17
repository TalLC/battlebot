import logging
from fastapi import FastAPI, Request
from common.ErrorCode import *
from common.config import CONFIG_REST
from business.GameManager import GameManager
from consumer.ConsumerManager import ConsumerManager
from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.commands.BotTurnCommand import BotTurnCommand
from business.gameobjects.entity.bots.commands.BotShootCommand import BotShootCommand
from consumer.brokers.messages.mqtt.ServerMqttIdMessage import ServerMqttIdMessage
from consumer.brokers.messages.stomp.ServerStompIdMessage import ServerStompIdMessage
from provider.security.NetworkSecurity import NetworkSecurity
from provider.security.NetworkSecurityDecorators import NetworkSecurityDecorators
from provider.webservices.rest.models.AdminBaseModel import AdminBaseModel
from provider.webservices.rest.models.AdminActionBanModel import AdminActionBanModel
from provider.webservices.rest.models.AdminActionUnbanModel import AdminActionUnbanModel
from provider.webservices.rest.models.AdminDisplayClientsActionListModel import AdminDisplayClientsActionListModel
from provider.webservices.rest.models.AdminDisplayClientsActionGetByIdModel import AdminDisplayClientsActionGetByIdModel
from provider.webservices.rest.models.AdminDisplayClientsActionGetByTokenModel import AdminDisplayClientsActionGetByTokenModel
from provider.webservices.rest.models.DisplayClientsActionReadyModel import DisplayClientsActionReadyModel
from provider.webservices.rest.models.BotsActionRegisterModel import BotsActionRegisterModel
from provider.webservices.rest.models.BotsIdActionCheckConnectionModel import BotsIdActionCheckConnectionModel
from provider.webservices.rest.models.BotsIdActionShootModel import BotsIdActionShootModel
from provider.webservices.rest.models.BotsIdActionTurnModel import BotsIdActionTurnModel
from provider.webservices.rest.models.BotsIdActionMoveModel import BotsIdActionMoveModel
from provider.webservices.rest.models.AdminActionSelectMapModel import AdminActionSelectMapModel


class RestProvider:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_endpoints()
        self.__admin_password = CONFIG_REST.admin_password

    def __register_endpoints(self):
        self.__admin_action_ban()
        self.__admin_action_unban()
        self.__admin_game_action_start()
        self.__admin_game_action_select_map()
        self.__admin_display_clients_action_list()
        self.__admin_display_clients_action_get_by_id()
        self.__admin_display_clients_action_get_by_token()
        self.__admin_bots_id_action_kill()
        self.__admin_bots_action_add()
        self.__display_action_ready()
        self.__bots_action_register()
        self.__bots_id_action_request_connection()
        self.__bots_id_action_check_connection()
        self.__bots_id_action_shoot()
        self.__bots_id_action_turn()
        self.__bots_id_action_move()
        logging.info("[REST] All endpoints registered")

    def __admin_action_ban(self):
        """
        Ban the specified IP from a specific source.
        """
        @self.__app.patch("/admin/action/ban")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: AdminActionBanModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Ban ip address
            banned_ip = NetworkSecurity().ban_ip(model.host, model.source, model.reason, model.definitive)
            return {'status': 'ok', 'banned': banned_ip.json()}

    def __admin_action_unban(self):
        """
        Unban the specified IP for a specific source.
        """
        @self.__app.patch("/admin/action/unban")
        async def action(model: AdminActionUnbanModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Ban ip address
            NetworkSecurity().unban_ip(model.host, model.source)
            return {'status': 'ok', 'message': f'{model.host} unbanned'}

    def __admin_game_action_start(self):
        """
        Start the current game.
        """
        @self.__app.patch("/game/action/start")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: AdminBaseModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            GameManager().start_game()
            return {'status': 'ok', 'message': 'Game is started'}

    def __admin_game_action_select_map(self):
        """
        Select the map.
        """
        @self.__app.patch("/game/action/select_map")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: AdminActionSelectMapModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            GameManager().load_map(map_id=model.map_name)
            return {'status': 'ok', 'message': 'Map is loaded.'}

    def __display_action_ready(self):
        """
        Set the display client to ready if the tokens matches.
        !!Do not use "client_token" as Path parameter to avoid clients to set ready for others!!
        """
        @self.__app.patch("/display/clients/action/ready")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: DisplayClientsActionReadyModel, _: Request):
            # Checking if the token exists
            if not GameManager().display_manager.does_client_token_exists(model.login_id):
                ErrorCode.throw(DISPLAY_CLIENT_ID_DOES_NOT_EXISTS)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_token(model.login_id)

            # Setting client to Ready
            client.set_ready()

            return {'status': 'ok', 'message': 'Tokens are matching'}

    def __admin_display_clients_action_list(self):
        """
        List all present and past display clients.
        """
        @self.__app.get("/display/clients/action/list")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: AdminDisplayClientsActionListModel, _: Request):
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
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: AdminDisplayClientsActionGetByIdModel, _: Request):
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
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: AdminDisplayClientsActionGetByTokenModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Does display client exists
            if not GameManager().display_manager.does_client_token_exists(model.client_token):
                ErrorCode.throw(DISPLAY_BAD_TOKEN)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_token(model.client_token)

            return {'status': 'ok', 'client': client.json()}

    def __admin_bots_id_action_kill(self):
        """
        Kills the specified bot.
        """
        @self.__app.patch("/bots/{bot_id}/action/kill")
        async def action(bot_id: str, model: AdminBaseModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Is bot already dead
            if not bot.is_alive:
                ErrorCode.throw(BOT_IS_DEAD)

            bot.kill()

            return {"status": "ok", "message": "The bot has been killed", "bot_id": bot.id}

    def __admin_bots_action_add(self):
        """
        Adds an ai-less bot in the game.
        """
        @self.__app.patch("/bots/action/add")
        async def action(model: AdminBaseModel, _: Request):
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Check if the game is full
            if GameManager().is_full:
                ErrorCode.throw(GAME_IS_FULL)

            # Check if the game is started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            logging.debug("Adding a test bot:")
            bot_count = GameManager().bot_manager.get_bots_count()
            bot = GameManager().bot_manager.create_bot(f"BOT TEST {bot_count}", "warrior")
            del GameManager().bot_manager._BOTS[bot.id]

            # Forcing bot ID
            bot._id = f"0-0-0-0-{bot_count}"
            GameManager().bot_manager._BOTS[bot.id] = bot

            # Adding the bot to the least populated team
            team = sorted(GameManager().team_manager.get_teams(), key=lambda t: t.bot_count())[0]
            team.add_bot(bot)

            bot.client_connection.connect(
                bot.client_connection.source_request_id,
                bot.client_connection.source_stomp_id,
                bot.client_connection.source_mqtt_id
            )

            return {"status": "ok", "message": "The bot has been added", "bot_id": bot.id}

    def __bots_action_register(self):
        """
        Create a new bot object and adds it to the specified team.
        """
        @self.__app.post("/bots/action/register")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(model: BotsActionRegisterModel, _: Request):

            # Check if the game is full
            if GameManager().is_full:
                ErrorCode.throw(GAME_IS_FULL)

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            bot_type = model.bot_type.lower()

            # Does team exists?
            if not GameManager().team_manager.does_team_exists(model.team_id):
                ErrorCode.throw(TEAM_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.create_bot(model.bot_name, bot_type)

            # Is bot alive
            if not bot.is_alive:
                ErrorCode.throw(BOT_IS_DEAD)

            # Adding the bot to the team
            is_bot_added = GameManager().team_manager.get_team(model.team_id).add_bot(bot)
            if not is_bot_added:
                ErrorCode.throw(TEAM_IS_FULL)

            logging.debug(f'[REST] Bot "{model.bot_name}" has been registered')

            return {"status": "ok", "message": "The bot has been successfully registered", "bot_id": bot.id}

    def __bots_id_action_request_connection(self):
        """
        Request connection ids to validate the connection to all the services.
        It sends 3 ids to the client using Rest, STOMP and MQTT.
        The client must send back these ids to the server to validate the connection.
        """
        @self.__app.get("/bots/{bot_id}/action/request_connection")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(bot_id: str, _: Request):
            logging.info(f"[REST] Bot {bot_id} is requesting a connection")

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Is bot alive
            if not bot.is_alive:
                ErrorCode.throw(BOT_IS_DEAD)

            # Sending 3 different ids to the client using 3 different channels
            # Rest, STOMP and MQTT
            ConsumerManager().mqtt.send_message(ServerMqttIdMessage(bot.id, bot.client_connection.source_mqtt_id))
            ConsumerManager().stomp.send_message(ServerStompIdMessage(bot.id, bot.client_connection.source_stomp_id))

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
        @NetworkSecurityDecorators.rest_ban_check
        async def action(bot_id: str, model: BotsIdActionCheckConnectionModel, _: Request):

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Compare rest ID
            if bot.client_connection.source_request_id != model.rest_id:
                ErrorCode.throw(LOGIN_INVALID_REQUEST_ID)

            # Compare STOMP ID
            if bot.client_connection.source_stomp_id != model.stomp_id:
                ErrorCode.throw(LOGIN_INVALID_STOMP_ID)

            # Compare MQTT ID
            if bot.client_connection.source_mqtt_id != model.mqtt_id:
                ErrorCode.throw(LOGIN_INVALID_MQTT_ID)

            # Connecting the bot
            bot.client_connection.connect(model.rest_id, model.stomp_id, model.mqtt_id)
            bot.send_client_bot_properties()
            return {"status": "ok", "message": "Your bot is successfully connected"}

    def __bots_id_action_shoot(self):
        """
        Make the bot shoot to the desired relative angle.
        """
        @self.__app.patch("/bots/{bot_id}/action/shoot")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(bot_id: str, model: BotsIdActionShootModel, _: Request):

            # Check if the game is not started
            if not GameManager().is_started:
                ErrorCode.throw(GAME_NOT_STARTED)

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Is bot alive
            if not bot.is_alive:
                ErrorCode.throw(BOT_IS_DEAD)

            # Is bot stunned
            if bot.is_stunned:
                ErrorCode.throw(BOT_IS_STUNNED)

            # Weapon unavailable
            if not bot.equipment.weapon.can_shoot:
                ErrorCode.throw(BOT_WEAPON_UNAVAILABLE)

            # Sending shoot command to the bot
            bot.add_command_to_queue(BotShootCommand(value=model.angle))

            return {"status": "ok", "message": f"Fired at {model.angle}°"}

    def __bots_id_action_turn(self):
        """
        Start to turn the specified bot to its left or right.
        """
        @self.__app.patch("/bots/{bot_id}/action/turn")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(bot_id: str, model: BotsIdActionTurnModel, _: Request):

            # Check if the game is not started
            if not GameManager().is_started:
                ErrorCode.throw(GAME_NOT_STARTED)

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Is bot alive
            if not bot.is_alive:
                ErrorCode.throw(BOT_IS_DEAD)

            # Is bot stunned
            if bot.is_stunned:
                ErrorCode.throw(BOT_IS_STUNNED)

            # Sending turn command to the bot
            bot.add_command_to_queue(BotTurnCommand(value=model.direction))

            if model.direction.lower() in ["left", "right"]:
                return {"status": "ok", "message": f"Bot is starting to turn {model.direction}"}
            elif model.direction.lower() == 'stop':
                return {"status": "ok", "message": "Bot has stopped turning"}

    def __bots_id_action_move(self):
        """
        Start to move the specified bot forward.
        """
        @self.__app.patch("/bots/{bot_id}/action/move")
        @NetworkSecurityDecorators.rest_ban_check
        async def action(bot_id: str, model: BotsIdActionMoveModel, _: Request):

            # Check if the game is not started
            if not GameManager().is_started:
                ErrorCode.throw(GAME_NOT_STARTED)

            # Does bot exists
            if not GameManager().bot_manager.does_bot_exists(bot_id):
                ErrorCode.throw(BOT_DOES_NOT_EXISTS)

            # Fetching corresponding Bot
            bot = GameManager().bot_manager.get_bot(bot_id)

            # Is bot alive
            if not bot.is_alive:
                ErrorCode.throw(BOT_IS_DEAD)

            # Is bot stunned
            if bot.is_stunned:
                ErrorCode.throw(BOT_IS_STUNNED)

            # Sending move command to the bot
            bot.add_command_to_queue(BotMoveCommand(value=model.action))

            if model.action == 'start':
                return {"status": "ok", "message": "Bot is starting to move"}
            elif model.action == 'stop':
                return {"status": "ok", "message": "Bot has stopped moving"}
