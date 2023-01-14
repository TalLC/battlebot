import logging
from fastapi import FastAPI
from common.config import CONFIG_TEAMS
from consumer.ConsumerManager import ConsumerManager
from provider.ProviderManager import ProviderManager
from provider.security.NetworkSecurity import NetworkSecurity
from business.GameManager import GameManager

"""
    Main script that starts all services.
"""

# Logging
# # Removing "uvicorn" duplicate logging
# # https://github.com/encode/uvicorn/issues/1285
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.removeHandler(uvicorn_logger.handlers[0])

# # Setting up basic logging config
logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                    format='[%(levelname)s] %(asctime)s - %(message)s')


app = FastAPI()  # Entry point for Uvicorn


@app.on_event('startup')
async def startup() -> None:
    # Teams
    for team in CONFIG_TEAMS:
        GameManager().team_manager.create_team(team.size, team.name, team.color, team.id)

    for team in GameManager().team_manager.get_teams():
        print(team)

    # Services
    # # Starting consumer services
    logging.info("[MAIN] Starting consumer services")
    ConsumerManager().start_all()

    # # Starting provider services
    logging.info("[MAIN] Starting provider services")
    NetworkSecurity()  # Initializing ban ip module
    provider_manager = ProviderManager(app)
    provider_manager.start_all()

    # DEBUG: BOT de test
    print("Enrôlement d'un bot de test :")
    bot = GameManager().bot_manager.create_bot("BOT TEST 01", "warrior")
    bot._id = "0-0-0-0-0"
    GameManager().team_manager.get_team("test-team-no-ai").add_bot(bot)
    GameManager().bot_manager._BOTS = dict()
    GameManager().bot_manager._BOTS[bot._id] = bot
    bot.client_connection.connect(
        bot.client_connection.source_request_id,
        bot.client_connection.source_stomp_id,
        bot.client_connection.source_mqtt_id
    )
    bot.set_position(15.5, 15.5, 0.0)

    print(GameManager().bot_manager.get_bot("0-0-0-0-0"))
    ##########################################


@app.on_event('shutdown')
def shutdown() -> None:
    NetworkSecurity().stop_thread()

