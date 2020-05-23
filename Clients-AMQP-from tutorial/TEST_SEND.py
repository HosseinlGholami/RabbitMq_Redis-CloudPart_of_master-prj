import pika
import time
credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
for i in range (3):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    message = "salaam."+str(i)
    channel.basic_publish(exchange='ex.mqtt', routing_key='', body=message)          
    
    print(" [x] Sent %r" % message)
    connection.close()
    time.sleep(0.1)

