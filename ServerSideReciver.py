
import threading 
import ctypes 
import time 
import pika

class MyThread(threading.Thread): 
  
    # Thread class with a _stop() method.  
    # The thread itself has to check 
    # regularly for the stopped() condition. 
  
    def __init__(self,Slug,Parameter,Packet2Handel,QueueName,CalbackFunc,*args, **kwargs): 
        super(MyThread, self).__init__(*args, **kwargs) 
        self.slug=Slug
        self.parameters=Parameter
        self.pckh=Packet2Handel
        self.queuename=QueueName
        self.callbackfunc=CalbackFunc


    def run(self): 
        # target function of the thread class 
        try: 
            connection = pika.BlockingConnection(self.parameters)
            channel = connection.channel()
            channel.basic_qos(prefetch_count=self.pckh)
            channel.basic_consume(queue=self.queuename,
                          on_message_callback=self.callbackfunc,
                          consumer_tag=self.slug)
            print('Theared 1 [*] Waiting for messages.')
            channel.start_consuming()
        finally: 
            # channel.stop_consuming()
            # channel.close()
            # connection.close()
            print('ended') 
           
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def stop(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 
       



#________________________________________________________________________

def callback(ch, method, properties, body):
     print("Received"+body.decode("utf-8") +" from :" +method.consumer_tag)
     time.sleep(1)
     ch.basic_ack(delivery_tag = method.delivery_tag)

credentials = pika.PlainCredentials('hgh', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)


t1 = MyThread(Slug='t1',Parameter=parameters,
              Packet2Handel=2,
              QueueName='classic_queue_2',
              CalbackFunc=callback
              )

t2 = MyThread(Slug='t2',Parameter=parameters,
              Packet2Handel=2,
              QueueName='classic_queue_2',
              CalbackFunc=callback
              )
# t1.start() 
# time.sleep(2) 
# t1.stop() 
# t1.join() 