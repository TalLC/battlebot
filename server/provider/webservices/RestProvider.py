import logging
from time import sleep
from fastapi import FastAPI, Request
from common.ErrorCode import *
from common.config import CONFIG_REST, refresh_config
from common.PerformanceCounter import PerformanceCounter
from business.GameManager import GameManager
from consumer.ConsumerManager import ConsumerManager
from business.gameobjects.entity.bots.commands.BotMoveCommand import BotMoveCommand
from business.gameobjects.entity.bots.commands.BotTurnCommand import BotTurnCommand
from business.gameobjects.entity.bots.commands.BotShootCommand import BotShootCommand
from consumer.brokers.messages.mqtt.ServerMqttIdMessage import ServerMqttIdMessage
from consumer.brokers.messages.stomp.ServerStompIdMessage import ServerStompIdMessage
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
from provider.webservices.rest.models.AdminActionSelectMapModel import AdminActionSelectMapModel
from consumer.webservices.messages.websocket.DisplayRefreshMessage import DisplayRefreshMessage


class RestProvider:
    tags_metadata = [
        # {"name": "unused", "description": "🚧 Unused or WIP"},
        {"name": "admin", "description": "🛡️ Requires API password"},
        {"name": "game", "description": "Game"},
        {"name": "display", "description": "Display"},
        {"name": "bots", "description": "Bots"},
        {"name": "teams", "description": "Teams"},
    ]

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__app.openapi_tags += self.tags_metadata
        self.__register_endpoints()
        self.__admin_password = CONFIG_REST.admin_password

    def __register_endpoints(self):
        self.__admin_game_action_new()
        self.__admin_game_action_reset()
        self.__admin_game_action_select_map()
        self.__game_maps_info()
        self.__admin_display_clients_action_list()
        self.__admin_display_clients_action_get_by_id()
        self.__admin_display_clients_action_get_by_token()
        self.__display_action_ready()
        self.__admin_bot_id_action_kill()
        self.__admin_bots_action_list()
        self.__admin_bots_action_add()
        self.__bots_action_register()
        self.__bots_id_action_request_connection()
        self.__bots_id_action_check_connection()
        self.__bots_id_action_shoot()
        self.__bots_id_action_turn()
        self.__bots_id_action_move()
        self.__admin_team_id_action_get_by_id()
        self.__admin_teams_action_list()
        logging.info("[REST] All endpoints registered")

    def __admin_game_action_new(self):
        @self.__app.post("/game/action/new", tags=['admin', 'game'])
        async def action(model: AdminBaseModel, _: Request):
            """
            Start the game.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            if GameManager().game_map is None:
                ErrorCode.throw(GAME_NO_MAP_SELECTED)

            if not GameManager().map_manager.does_map_exists(map_id=GameManager().game_map.id):
                ErrorCode.throw(GAME_MAP_DOES_NOT_EXISTS)

            GameManager().new_game()
            return {'status': 'ok', 'message': 'Game is starting'}

    def __admin_game_action_reset(self):
        @self.__app.post("/game/action/reset", tags=['admin', 'game'])
        async def action(model: AdminBaseModel, _: Request):
            """
            Resets the game as if the server was restarted.
            This is usually called from the frontend using some key combination.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Stop the game if started
            if GameManager().is_started:
                GameManager().stop_game()
                while GameManager().is_started:
                    sleep(100/1000)

            # Send a refresh page message to display clients
            for client in GameManager().display_manager.get_clients():
                try:
                    if client.websocket.client_state.CONNECTED:
                        await client.websocket.send_json(DisplayRefreshMessage().json())
                except RuntimeError:
                    logging.exception("Socket was closed before it could send refresh message")
                except:
                    logging.exception("Error while closing socket or sending the refresh message")
            sleep(1)

            # Reload config files
            refresh_config()

            # Disconnect and remove all display clients
            await GameManager().display_manager.reset()

            return {'status': 'ok', 'message': 'Game has been reset'}

    def __admin_game_action_select_map(self):
        @self.__app.post("/game/maps/{map_id}/select", tags=['admin', 'game'])
        async def action(map_id: str, model: AdminBaseModel, _: Request):
            """
            Set the game map.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Check if the game is already started
            if GameManager().is_started:
                ErrorCode.throw(GAME_ALREADY_STARTED)

            if not GameManager().map_manager.does_map_exists(map_id=map_id):
                ErrorCode.throw(GAME_MAP_DOES_NOT_EXISTS)

            GameManager().load_map(map_id=map_id)
            return {'status': 'ok', 'message': 'Map is loaded.'}

    def __game_maps_info(self):
        @self.__app.get("/game/maps/{map_id}/info", tags=['game'])
        async def action(map_id: str, _: Request):
            """
            Get map information.
            """
            return GameManager().map_manager.get_map(map_id).metadata

    def __display_action_ready(self):
        """
        !!Do not use "client_token" as Path parameter to avoid clients to set ready for others!!
        """
        @self.__app.patch("/display/clients/action/ready", tags=['display'])
        async def action(model: DisplayClientsActionReadyModel, _: Request):
            """
            Set the display client to ready if the tokens matches.
            """
            # Checking if the token exists
            if not GameManager().display_manager.does_client_token_exists(model.login_id):
                ErrorCode.throw(DISPLAY_CLIENT_ID_DOES_NOT_EXISTS)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_token(model.login_id)

            # Setting client to Ready
            client.set_ready()

            return {'status': 'ok', 'message': 'Tokens are matching'}

    def __admin_display_clients_action_list(self):
        @self.__app.get("/display/clients/action/list", tags=['admin', 'display'])
        async def action(model: AdminDisplayClientsActionListModel, _: Request):
            """
            List all present and past display clients.
            """
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
        @self.__app.get("/display/clients/action/get_by_id", tags=['admin', 'display'])
        async def action(model: AdminDisplayClientsActionGetByIdModel, _: Request):
            """
            Find a display client by its id.
            """
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
        @self.__app.get("/display/clients/action/get_by_token", tags=['admin', 'display'])
        async def action(model: AdminDisplayClientsActionGetByTokenModel, _: Request):
            """
            Find a display client by its token.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Does display client exists
            if not GameManager().display_manager.does_client_token_exists(model.client_token):
                ErrorCode.throw(DISPLAY_BAD_TOKEN)

            # Fetching corresponding display client
            client = GameManager().display_manager.get_client_by_token(model.client_token)

            return {'status': 'ok', 'client': client.json()}

    def __admin_bot_id_action_kill(self):
        @self.__app.patch("/bots/{bot_id}/action/kill", tags=['admin', 'bots'])
        async def action(bot_id: str, model: AdminBaseModel, _: Request):
            """
            Kills the specified bot.
            """
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

    def __admin_bots_action_list(self):
        @self.__app.get("/bots/action/list", tags=['admin', 'bots'])
        async def action(model: AdminBaseModel, _: Request):
            """
            List all bots in the game.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            result = list()
            for bot in GameManager().bot_manager.get_bots(connected_only=False, alive_only=False):
                result.append(bot.json())

            return {"status": "ok", "bots": result}

    def __admin_bots_action_add(self):
        @self.__app.patch("/bots/action/add", tags=['admin', 'bots'])
        async def action(model: AdminBaseModel, _: Request):
            """
            Adds an ai-less bot in the game.
            """
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
        @self.__app.post("/bots/action/register", tags=['bots'])
        async def action(model: BotsActionRegisterModel, _: Request):
            """
            Create a new bot object and adds it to the specified team.
            """
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
        @self.__app.get("/bots/{bot_id}/action/request_connection", tags=['bots'])
        async def action(bot_id: str, _: Request):
            """
            Request connection ids to validate the connection to all the services.
            It sends 3 ids to the client using Rest, STOMP and MQTT.
            The client must send back these ids to the server to validate the connection.
            """
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
        @self.__app.patch("/bots/{bot_id}/action/check_connection", tags=['bots'])
        async def action(bot_id: str, model: BotsIdActionCheckConnectionModel, _: Request):
            """
            Check if the ids found by the client are the expected ones in order to validate the client connection to all
            our services.
            """
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
        @self.__app.patch("/bots/{bot_id}/action/shoot", tags=['bots'])
        @PerformanceCounter.count
        async def action(bot_id: str, model: BotsIdActionShootModel, _: Request):
            """
            Make the bot shoot to the desired relative angle.
            """
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
        @self.__app.patch("/bots/{bot_id}/action/turn", tags=['bots'])
        @PerformanceCounter.count
        async def action(bot_id: str, model: BotsIdActionTurnModel, _: Request):
            """
            Start to turn the specified bot to its left or right.
            """
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
        @self.__app.patch("/bots/{bot_id}/action/move", tags=['bots'])
        @PerformanceCounter.count
        async def action(bot_id: str, model: BotsIdActionMoveModel, _: Request):
            """
            Start to move the specified bot forward.
            """
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

    def __admin_team_id_action_get_by_id(self):
        @self.__app.get("/teams/{team_id}", tags=['admin', 'teams'])
        async def action(team_id: str, model: AdminBaseModel, _: Request):
            """
            Find a team by its id.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            # Does team exists
            if GameManager().team_manager.get_team(team_id=team_id) is None:
                ErrorCode.throw(DISPLAY_CLIENT_ID_DOES_NOT_EXISTS)

            # Fetching corresponding team
            team = GameManager().team_manager.get_team(team_id=team_id)

            return {'status': 'ok', 'team': team.json()}

    def __admin_teams_action_list(self):
        @self.__app.get("/teams/action/list", tags=['admin', 'teams'])
        async def action(model: AdminBaseModel, _: Request):
            """
            List all teams in the game.
            """
            # Check the admin password
            if model.api_password != self.__admin_password:
                ErrorCode.throw(ADMIN_BAD_PASSWORD)

            result = list()
            for team in GameManager().team_manager.get_teams(alive_only=False):
                result.append(team.json())

            return {"status": "ok", "teams": result}
