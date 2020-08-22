from util import init , active_sLs 


number_of_SL=1

parameters=init()

h=active_sLs(number_of_SL,parameters,5,'classic_queue_1')



def stop_all(handler):
    for i in handler:
        i.stop()