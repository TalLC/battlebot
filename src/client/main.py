import logging
import requests
from time import sleep
from pathlib import Path
import json
from MQTTClient import MQTTClient
from STOMPClient import STOMPClient


G_SETTINGS = json.loads(Path("settings.json").read_text())
G_TEAM_ID = G_SETTINGS['team_id']
G_BOT_NAME = G_SETTINGS['bot_name']

G_REST_SETTINGS = G_SETTINGS["rest"]
G_MQTT_SETTINGS = G_SETTINGS["mqtt"]
G_STOMP_SETTINGS = G_SETTINGS["stomp"]
G_REST_URL = f"{G_REST_SETTINGS['protocol']}://{G_REST_SETTINGS['host']}:{G_REST_SETTINGS['port']}"

G_CONNECTION_STATUS = {
    "request_id": str(),
    "stomp_id": str(),
    "mqtt_id": str()
}


def request_connection(bot_id: str):
    """
    Check Rest, MQTT and STOMP connections.
    """
    r = requests.get(G_REST_URL + f"/bots/{bot_id}/action/request_connection")
    if r.ok:
        if 'request_id' in r.json():
            G_CONNECTION_STATUS["request_id"] = r.json()['request_id']

    if G_CONNECTION_STATUS["request_id"] in [str(), None]:
        raise Exception("Unable to find Rest 'request_id'")


def read_mqtt_id():
    """
    Read mqtt_id from MQTT.
    """
    def on_message(_client, _userdata, msg: MQTTClient.MQTTMessage):
        message = message_to_dict(msg.payload.decode('utf-8'), msg.topic)
        if message == dict():
            return

        if 'mqtt_id' in message:
            G_CONNECTION_STATUS["mqtt_id"] = message['mqtt_id']

    mqtt = MQTTClient(
        G_MQTT_SETTINGS['host'], G_MQTT_SETTINGS['port'], G_MQTT_SETTINGS['username'], G_MQTT_SETTINGS['password']
    )

    logging.debug(f"Subscribing to {G_MQTT_SETTINGS['queue_head'] + bot_id}")
    mqtt.subscribe(G_MQTT_SETTINGS['queue_head'] + bot_id)
    mqtt.on_message(on_message)

    # Waiting for mqtt_id message
    mqtt_timeout = 10
    while G_CONNECTION_STATUS["mqtt_id"] in [str(), None] and mqtt_timeout > 0:
        mqtt.loop()
        sleep(1)
        mqtt_timeout -= 1

    # Check if the message has been read and the id found
    if G_CONNECTION_STATUS["mqtt_id"] in [str(), None]:
        raise Exception("Unable to find MQTT messages")


def read_stomp_id():
    """
    Read stomp_id from STOMP.
    """
    class Listener(STOMPClient.ConnectionListener):
        @staticmethod
        def on_error(frame: STOMPClient.Frame):
            logging.error(f'Reader : received an error {frame}')

        @staticmethod
        def on_message(frame: STOMPClient.Frame):
            message = message_to_dict(
                frame.body,
                frame.headers['destination'] if 'destination' in frame.headers else str()
            )
            if message == dict():
                return

            if 'stomp_id' in message:
                G_CONNECTION_STATUS["stomp_id"] = message['stomp_id']

    stomp = STOMPClient(
        G_STOMP_SETTINGS['host'], G_STOMP_SETTINGS['port'], G_STOMP_SETTINGS['username'], G_STOMP_SETTINGS['password']
    )

    logging.debug(f"Subscribing to {G_STOMP_SETTINGS['queue_head'] + bot_id}")
    stomp.subscribe(G_STOMP_SETTINGS['queue_head'] + bot_id)
    stomp.set_listener("stomp listener", Listener())

    # Waiting for stomp_id message
    timeout = 10
    while G_CONNECTION_STATUS["stomp_id"] in [str(), None] and timeout > 0:
        sleep(1)
        timeout -= 1

    # Check if the message has been read and the id found
    if G_CONNECTION_STATUS["stomp_id"] in [str(), None]:
        raise Exception("Unable to find STOMP messages")


def send_ids_to_check(bot_id: str, request_id: str, stomp_id: str, mqtt_id: str) -> bool:
    """
    Validate connection by sending all requested ids.
    """
    payload = {
        'request_id': request_id,
        'stomp_id': stomp_id,
        'mqtt_id': mqtt_id
    }
    r = requests.patch(G_REST_URL + f"/bots/{bot_id}/action/check_connection", json=payload)
    if not r.ok:
        if 'detail' in r.json():
            raise Exception(r.json()['detail'])

    return r.ok


def enroll_new_bot(team_id: str, bot_name: str) -> str:
    """
    Enroll a new bot in team.
    """
    payload = {
        'team_id': team_id,
        'bot_name': bot_name
    }
    r = requests.post(G_REST_URL + f"/bots/action/register", json=payload)
    if r.ok:
        if "bot_id" in r.json():
            return r.json()["bot_id"]
    else:
        if 'detail' in r.json():
            raise Exception(r.json()['detail'])


def message_to_dict(msg: str, topic: str) -> dict:
    try:
        data = json.loads(msg)
    except json.decoder.JSONDecodeError:
        logging.error(f"Received invalid JSON: {msg}")
        return dict()

    logging.debug(f"Received `{data}` from `{topic}` topic")

    return data


if __name__ == "__main__":
    bot_id = ""

    # Logging
    logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # Enroll bot and get bot ID
    bot_id = bot_id if bot_id not in [str(), None] else enroll_new_bot(G_TEAM_ID, G_BOT_NAME)
    logging.info(f"Bot {bot_id} has been enrolled")

    # Check Rest, MQTT and STOMP connections
    request_connection(bot_id)
    logging.info(f"Rest id {G_CONNECTION_STATUS['request_id']} has been found")

    # Check if we find the messages in the STOMP and MQTT queues
    logging.debug(f"MQTT and STOMP messages have been requested")

    # MQTT
    read_mqtt_id()
    logging.info(f"MQTT id {G_CONNECTION_STATUS['mqtt_id']} has been found")

    # STOMP
    read_stomp_id()
    logging.info(f"STOMP id {G_CONNECTION_STATUS['stomp_id']} has been found")

    # Check if we have all the messages
    send_ids_to_check(
        bot_id,
        G_CONNECTION_STATUS["request_id"],
        G_CONNECTION_STATUS["stomp_id"],
        G_CONNECTION_STATUS["mqtt_id"]
    )

    logging.info("****************************************************************")
    logging.info("**         WEEEEEEEEEEEEEEEEEEEEE EVERYTHING WORKS!!!         **")
    logging.info("****************************************************************")
