import logging
from fastapi import FastAPI
from common.config import *
from common.PerformanceCounter import PerformanceCounter
from consumer.ConsumerManager import ConsumerManager
from provider.ProviderManager import ProviderManager
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
logging.basicConfig(level=logging.DEBUG if CONFIG_GAME.is_debug else logging.INFO,
                    datefmt='%d/%m/%Y %I:%M:%S', format='[%(levelname)s] %(asctime)s - %(message)s')

app = FastAPI()  # Entry point for Uvicorn
app.openapi_tags = list()


@app.on_event('startup')
async def startup() -> None:
    # Performance counter
    PerformanceCounter()

    # Services
    # # Starting consumer services
    logging.info("[MAIN] Starting consumer services")
    ConsumerManager().start_all()

    # # Starting provider services
    logging.info("[MAIN] Starting provider services")
    provider_manager = ProviderManager(app)
    provider_manager.start_all()

    # Init GameManager Singleton
    GameManager()


@app.on_event('shutdown')
def shutdown() -> None:
    PerformanceCounter().stop()
