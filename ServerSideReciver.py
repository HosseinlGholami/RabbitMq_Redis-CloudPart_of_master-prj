import pika
import time 
import threading 
  
class MyThread(threading.Thread): 
  
    # Thread class with a _stop() method.  
    # The thread itself has to check 
    # regularly for the stopped() condition. 
  
    def __init__(self,Parameter,Packet2Handel,QueueName,CalbackFunc,*args, **kwargs): 
        super(MyThread, self).__init__(*args, **kwargs) 
        self._stop = threading.Event() 
        self.parameters=Parameter
        self.pckh=Packet2Handel
        self.queuename=QueueName
        self.callbackfunc=CalbackFunc
    
        
    # function using _stop function 
    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet() 
  
    def run(self): 
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=self.pckh)
        channel.basic_consume(queue=self.queuename,
                      on_message_callback=self.callbackfunc)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        while(True):
            channel.start_consuming()
            channel.consume(queue)
            channel.stop_consuming()
            if self.stopped():
                return



https://pika.readthedocs.io/en/stable/examples/blocking_consumer_generator.html



def callback(ch, method, properties, body):
     print("Received %r" % body.decode("utf-8"))
     time.sleep(1)
     ch.basic_ack(delivery_tag = method.delivery_tag)

credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)


t1 = MyThread(Parameter=parameters,
              Packet2Handel=1,
              QueueName='classic_queue_2',
              CalbackFunc=callback
              )
    
# t1.start() 
# time.sleep(5) 
# t1.stop() 
# t1.join() 