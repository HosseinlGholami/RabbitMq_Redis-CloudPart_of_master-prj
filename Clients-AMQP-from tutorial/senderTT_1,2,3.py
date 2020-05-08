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
    
    message = "salaam."+str(i)
        #TT1,2 sent to default exchange and que
    # channel.basic_publish(exchange='',
    #                       routing_key='task_queue',
    #                       body=message,
    #                       properties=pika.BasicProperties(                    
    #                           delivery_mode = 2, # make message persistent
    #                          )
    #                       )
    
    
        #TTL3
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    #if we dont bined a exchange to consumer , the massge would be removed
    channel.basic_publish(exchange='logs', routing_key='', body=message)          
    
    
    print(" [x] Sent %r" % message)
    connection.close()
    time.sleep(0.1)



