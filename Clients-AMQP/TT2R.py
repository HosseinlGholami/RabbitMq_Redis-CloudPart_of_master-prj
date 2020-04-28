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

    #TT2
    #declare queue and make it durable ! means the massege wich are not recived 
    #should be recived if we dont set this flag , the previous massge which are 
    #stored in queue , will be removed
channel.queue_declare(queue='task_queue', durable=True)
    #if we add this line , its like we have load blacing and if we have 
    #idle consumer , we add some task to him 
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='task_queue',
                      on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
