import logging
import requests
from pathlib import Path
import json
import stomp
import paho.mqtt.client as mqtt


logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                    format='[%(levelname)s] %(asctime)s - %(message)s')

G_SETTINGS = json.loads(Path("settings.json").read_text())
G_TEAM_ID = G_SETTINGS['team_id']
G_BOT_NAME = G_SETTINGS['bot_name']

G_SRV_SETTINGS = G_SETTINGS["server"]
G_SERVER_URL = f"{G_SRV_SETTINGS['protocol']}://{G_SRV_SETTINGS['host']}:{G_SRV_SETTINGS['port']}"


def check_api() -> bool:
    """
    Check API connection.
    """
    r = requests.get(G_SERVER_URL + "/")
    return r.ok


def check_connection(bot_id: str) -> dict:
    """
    Check MQTT and STOMP connections.
    """
    r = requests.get(G_SERVER_URL + f"/check_connections?bot_id={bot_id}")
    if r.ok:
        return {
            "stomp_id": r.json()["stomp_id"],
            "mqtt_id": r.json()["mqtt_id"]
        }
    return dict()


def enroll(team_id: str, bot_name: str) -> str:
    r = requests.post(G_SERVER_URL + f"/registration?team_id={team_id}&bot_name={bot_name}")
    if r.ok:
        if "bot_id" in r.json():
            return r.json()["bot_id"]
    return str()


if __name__ == "__main__":
    # Test API
    if not check_api():
        raise "API is not available"

    logging.info("API is available")

    # Enroll bot and get bot ID
    bot_id = enroll(G_TEAM_ID, G_BOT_NAME)
    if bot_id == str() or bot_id is None:
        raise "Bot is not enrolled"

    logging.info(f"Bot {bot_id} has been enrolled")

    # Check MQTT and STOMP connections
    connections = check_connection(bot_id)
    if connections == dict() or connections is None:
        raise "API did not send STOMP and MQTT messages"

    mqtt_id = connections["mqtt_id"]
    stomp_id = connections["stomp_id"]
    logging.info(f"MQTT and STOMP messages have been requested")

    # Check if we find the messages in the STOMP and MQTT queues
    # TODO
