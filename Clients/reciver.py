import pika
import time

def callback(ch, method, properties, body):
     print("Received %r" % body.decode("utf-8"))
     time.sleep(int(body.decode("utf-8").split(".")[1]))
     print("Done")
     ch.basic_ack(delivery_tag = method.delivery_tag)

credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_consume(queue='task_queue',
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
