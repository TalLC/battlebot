#!/usr/bin/env python
import pika

# credentials = pika.PlainCredentials('user', 'bitnami')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='92.222.234.51', credentials=credentials))

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body=b'Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
