import sys
import stomp
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)


def connect_stomp(up, hp) -> stomp.Connection:
    conn = stomp.Connection(host_and_ports=hp)
    conn.connect(up, up, wait=True)

    return conn


def send_message(connexion, message):
    connexion.send(body='<message>compteur=%s<message>'.format(message), destination='stomptest')


def receive_message(connexion):
    connexion.subscribe('stomptest', 123)


if __name__ == '__main__':
    # settings
    userpass = "admin"
    hap = [("localhost", 61613)]
    count = 0

    # connect to broker
    stomp_co = connect_stomp(userpass, hap)

    # publisher
    while True:
        send_message(stomp_co, f"compteur = {count}")
        sleep(3)
        count += 1
