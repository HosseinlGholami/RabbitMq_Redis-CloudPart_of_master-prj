import pika
import time

def callback(ch, method, properties, body):
     print("Received %r" % body.decode("utf-8"))
     time.sleep(int(body.decode("utf-8").split(".")[1]))
     print("Done on %r"%(method.routing_key))
     

credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

#channel.exchange_declare(exchange='mamadi', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities=['a','b']
if not severities:
    print("mamad oon zz ro biar")
    
for severity in severities:
    channel.queue_bind(
        exchange='mamadi', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()





