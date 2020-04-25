import pika
import time
credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
for i in range (20):
        
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    message = "salam."+str(i)
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode = 2, # make message persistent
                             )
                          )
    print(" [x] Sent %r" % message)
    connection.close()
    time.sleep(0.1)



