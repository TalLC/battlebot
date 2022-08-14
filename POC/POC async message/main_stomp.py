import stomp
import logging
import json
from time import sleep


def connect_stomp(username=None, passcode=None, host: str = "localhost", port: int = 61613) -> stomp.Connection:
    conn = stomp.Connection(host_and_ports=[(host, port)])
    conn.connect(username=username, passcode=passcode, wait=True)
    return conn


def send_message(connection: stomp.Connection, destination: str, message: dict):
    connection.send(destination=destination, body=json.dumps(message))


def receive_message(connection: stomp.Connection):
    connection.subscribe(destination='stomptest', id=str(123))


if __name__ == '__main__':
    # logging
    logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # settings
    user = "user"
    pwd = "user"
    host = "localhost"
    port = 61613

    queue = "stomptest"

    # connect to broker
    stomp_co = connect_stomp(user, pwd, host, port)
    if not stomp_co.is_connected():
        raise "Failed to connect to broker"

    # publisher
    count = 0
    while True:
        send_message(stomp_co, queue, {'compteur': count})
        sleep(3)
        count += 1
