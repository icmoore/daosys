from python.dev.event import TokenEvent
import numpy as np
import queue

class Deposit(TokenEvent):
   
    TYPE_REBASE = 'REBASE'
    TYPE_NONREBASE = 'NONREBASE'  

    def __init__(self, apy, delta, t_delta, address = None):
        self.__t_delta = t_delta
        self.__delta = delta
        self.__apy = apy
        self.__address = address if address != None else address
        
    def get_time_delta(self, reset = False):
        return self.__getVal(self.__t_delta, reset) 
       
    def get_delta(self, reset = False):
        return self.__getVal(self.__delta, reset) 
    
    def get_apy(self, reset = False):
        return self.__getVal(self.__apy, reset) 

    def get_address(self):
        return self.__address
    
    def set_address(self, address):
        self.__address = address
        
    def set_delta(self, delta):
        self.__delta = delta     
        
    def set_time_delta(self, time_delta):
        self.__t_delta = time_delta          
    
    def type_of(self):
        return TokenEvent.EVENT_DEPOSIT   
        
    def __isQueue(self, obj):
        return type(obj) == queue.Queue 

    def __isNumeric(self, obj):  
        return type(obj) == int or type(obj) == float or type(obj) == np.float64 or type(obj) == np.int64

    def __getVal(self, obj, reset = False):
        if(self.__isNumeric(obj)):
            return obj
        elif(self.__isQueue(obj)):
            return obj.get() if reset else obj.queue[0]
        else: 
            return None