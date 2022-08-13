import logging
import json
from pathlib import Path
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
logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                    format='[%(levelname)s] %(asctime)s - %(message)s')


# Configuration files
# # Team configuration
G_CONF_DIR = "conf"
G_CONF_FILE_TEAMS = Path(G_CONF_DIR, "teams.json")
G_CONF_TEAMS = json.loads(G_CONF_FILE_TEAMS.read_text())

# # Adding Teams
for team in G_CONF_TEAMS:
    t = GameManager().add_team(team["size"], team["name"], team["color"], team["id"] if "id" in team else None)
    print(t)


# Services
# # Starting provider services
logging.info("Starting provider services")
provider_manager = ProviderManager()  # Entry point for Uvicorn
provider_manager.start_all()
