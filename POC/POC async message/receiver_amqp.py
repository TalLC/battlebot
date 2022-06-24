#!/usr/bin/env python
import os
import pika
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    credentials = pika.PlainCredentials('admin', 'admin')
    print('co param')
    co_param = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    print('connection')
    connection = pika.BlockingConnection(co_param)
    print('channel')
    channel = connection.channel()
    print('queue_declare')
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
