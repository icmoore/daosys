from python.dev.event import TokenEvent

class Rebase(TokenEvent):
    
    def __init__(self, apy, t_delta, address = None):
        self.__t_delta = t_delta
        self.__delta = 0
        self.__apy = apy
        self.__address = address if address != None else address
        
    def get_time_delta(self):
        return self.__t_delta
       
    def get_delta(self):
        return self.__delta
    
    def get_apy(self):
        return self.__apy

    def get_address(self):
        return self.__address
    
    def set_delta(self, delta):
        self.__delta = delta     
        
    def set_time_delta(self, time_delta):
        self.__t_delta = time_delta     
    
    def type_of(self):
        return TokenEvent.EVENT_REBASE