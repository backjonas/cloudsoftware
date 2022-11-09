#!/usr/bin/env python
import pika
import sys
import os
import time

def main():
  def callback(ch, method, properties, body):
    print(" [x] %r" % body)

  connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

  channel = connection.channel()
  channel.exchange_declare(exchange='logs', exchange_type='fanout')

  result = channel.queue_declare(queue='', exclusive=True)
  queue_name = result.method.queue
  channel.queue_bind(exchange='logs', queue=queue_name)

  channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

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