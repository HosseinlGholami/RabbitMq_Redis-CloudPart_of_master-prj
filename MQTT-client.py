#know that Topic is roating key!

import pika
import time

def callback(ch, method, properties, body):
     print("Received %r" % body.decode("utf-8"))
     time.sleep(1)
     ch.basic_ack(delivery_tag = method.delivery_tag)

credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()


channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='classic_queue_2',
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
