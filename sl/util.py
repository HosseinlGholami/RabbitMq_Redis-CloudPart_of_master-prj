import pika
import time
import threading 
import ctypes
import pandas as pd
from pandas import json_normalize
import json
import redis


def init(): 
    time.sleep(15)
    #pika initialization
    credentials = pika.PlainCredentials('CNSMR', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq',
                                       5672,
                                       '/',
                                       credentials)
    return parameters

class rbmq(threading.Thread): 
    # Thread class with a _stop() method.  
    # The thread itself has to check 
    # regularly for the stopped() condition. 
    def __init__(self,Slug,Parameter,prefetch_count,QueueName,CalbackFunc,*args, **kwargs): 
        super(rbmq, self).__init__(*args, **kwargs) 
        self.slug=Slug
        self.parameters=Parameter
        self.pckh=prefetch_count
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
            print( self.slug ,' [*] Waiting for messages on :',self.queuename )
            channel.start_consuming()
        finally: 
            connection.close()
            print(self.slug ,'  Stoped from ',self.queuename )
           
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
       
    
def Packet_Handeler_callback(ch, method, properties, body):
    Str=str(body.decode("utf-8"))
    Data=json.loads(Str)
    client = redis.Redis(host='redis', port=6379)
    send_correct = client.hset(name=Data['driver_id'],key=Data['timestamp'],value=Data['event'])
    print('Data_from: ',Data['driver_id'])
    #save Fails in log file 
    if not(send_correct):
        with open(".//log//log.txt", "a") as myfile :
            myfile.write(Str)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def CreateSL(consumer_tag,parameters,prefetch_count,Queue_Name):
    return rbmq(Slug=consumer_tag,
                Parameter=parameters,
                prefetch_count=prefetch_count,
                QueueName=Queue_Name,
                CalbackFunc=Packet_Handeler_callback
                )

                
def active_sLs(number_of_SL,parameters,prefetch_count,Queue_Name):
    handler=list()
    for consumer_tag in range(number_of_SL):
        x=CreateSL(str(consumer_tag), parameters, prefetch_count, Queue_Name)
        handler.append(x)
        x.start()
        time.sleep(0.1)
    return handler
