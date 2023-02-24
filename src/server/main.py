import logging
from fastapi import FastAPI
from common.config import CONFIG_DEBUG, CONFIG_TEAMS
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
logging.basicConfig(level=logging.DEBUG if CONFIG_DEBUG.is_debug else logging.INFO,
                    datefmt='%d/%m/%Y %I:%M:%S', format='[%(levelname)s] %(asctime)s - %(message)s')


app = FastAPI()  # Entry point for Uvicorn


@app.on_event('startup')
async def startup() -> None:
    # Teams
    for team in CONFIG_TEAMS:
        GameManager().team_manager.create_team(team.size, team.name, team.color, team.id)

    logging.info("[MAIN] Created teams:")
    for team in GameManager().team_manager.get_teams():
        logging.info(team)

    # Services
    # # Starting consumer services
    logging.info("[MAIN] Starting consumer services")
    ConsumerManager().start_all()

    # # Starting provider services
    logging.info("[MAIN] Starting provider services")
    NetworkSecurity()  # Initializing ban ip module
    provider_manager = ProviderManager(app)
    provider_manager.start_all()


@app.on_event('shutdown')
def shutdown() -> None:
    NetworkSecurity().stop_thread()

