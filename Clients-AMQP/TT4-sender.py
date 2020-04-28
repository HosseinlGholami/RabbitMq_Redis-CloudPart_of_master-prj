import pika
import time
credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)
for i in range (10):
        
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    channel.exchange_declare(exchange='mamadi', exchange_type='direct')
    
    st={0:'a',1:'b',2:'zzz'}
    rk=st[i%3]
    message = "salaam."+str(i)
    
    channel.basic_publish(exchange="mamadi", routing_key=rk,body=message)
    
    print(" [x] Sent %r" % message)
    print(" [x] Sent %r" % rk)
    
    connection.close()
    time.sleep(0.1)



