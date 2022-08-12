from python.dev.event import Deposit
import queue

class DepositQueue(Deposit):
   
    TYPE_REBASE = 'REBASE'
    TYPE_NONREBASE = 'NONREBASE'  

    def __init__(self, apy, delta, t_delta, address = None):
        self.__t_delta = t_delta
        self.__delta = delta
        self.__apy = apy
        self.__address = address if address != None else address
        
    def get_time_delta(self):
        return self._getVal(self.__t_delta) 
       
    def get_delta(self):
        return self._getVal(self.__delta)  
    
    def get_apy(self):
        return self._getVal(self.__apy) 

    def get_address(self):
        return self.__address
    
    def set_address(self, address):
        self.__address = address      
    
    def type_of(self):
        return TokenEvent.EVENT_DEPOSIT   
        
    def _isQueue(self, obj):
        return type(obj) == queue.Queue 

    def _isNumeric(self, obj):  
        return type(obj) == int or type(obj) == float

    def _getVal(self, obj):
        if(self._isNumeric(obj)):
            return obj
        elif(self._isQueue(obj)):
            return obj.get() 
        else 
            return None