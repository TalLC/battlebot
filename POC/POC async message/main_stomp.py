import stomp
from threading import Thread, Event
from stomp.utils import Frame
import logging
import json
from time import sleep


def connect_stomp(username=None, passcode=None, host: str = "localhost", port: int = 61613) -> stomp.Connection:
    conn = stomp.Connection(host_and_ports=[(host, port)])
    conn.connect(username=username, passcode=passcode, wait=True)
    return conn


class Listener(stomp.ConnectionListener):
    """
    Callback for when a STOMP frame is received.
    """
    def on_error(self, frame: Frame):
        print(f'received an error {frame}')

    def on_message(self, frame: Frame):
        print(f'Reader : receiving message {frame.body}')


def send_messages(connection: stomp.Connection, e: Event):
    # Continuous publishing to queue
    msg_count = 0

    while not e.is_set():
        print(f'Writer : Sending message n°{msg_count}')
        connection.send(destination=queue, body=json.dumps({'compteur': msg_count}))
        sleep(3)
        msg_count += 1

    stomp_co_writer.disconnect()
    print("Writer disconnected")


if __name__ == '__main__':
    # logging
    logging.basicConfig(level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S',
                        format='[%(levelname)s] %(asctime)s - %(message)s')

    # Settings
    host = "localhost"
    port = 61613
    queue = "BOT.stomptest"

    # Creating a connection that will push messages to the queue
    # Connect to broker
    event = Event()

    stomp_co_writer = connect_stomp("system", "manager", host, port)
    if not stomp_co_writer.is_connected():
        raise "Failed to connect to broker"

    # Publish to queue
    Thread(target=send_messages, args=(stomp_co_writer, event)).start()

    # Creating a connection that will read messages from the queue
    # Settings
    connection_number = 0

    # Connect to broker
    stomp_co_reader = connect_stomp("user", "password", host, port)
    if not stomp_co_reader.is_connected():
        raise "Failed to connect to broker"

    # Subscribe to queue
    connection_number += 1  # obligatoire, car plusieurs queues peuvent être subscribe
    stomp_co_reader.subscribe(destination=queue, id=str(connection_number))
    stomp_co_reader.set_listener('ActiveMQ Stomp Listener', Listener())

    # Waiting for cancellation
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        event.set()
    finally:
        stomp_co_reader.disconnect()
        print("Reader disconnected")
