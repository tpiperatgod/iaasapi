#!/usr/bin/env python
import pika
import config as FLAG

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=FLAG.RABBITMQ_IP))

channel = connection.channel()

channel.exchange_declare(exchange=FLAG.RABBITMQ_EXCHANGE, type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=FLAG.RABBITMQ_EXCHANGE, queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] %r" % body

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
