from python.dev.event import TokenEvent


class Swap(TokenEvent):
   
    def __init__(self, withdraw_event, deposit_event):
        self.__t_delta = max(withdraw_event.get_time_delta(), deposit_event.get_time_delta())
        self.__delta = deposit_event.get_delta()
        self.__apy = deposit_event.get_apy()
        self.__from_address = deposit_event.get_address() 
        self.__to_address = deposit_event.get_address()
        
    def get_time_delta(self):
        return self.__t_delta
       
    def get_delta(self):
        return self.__delta
    
    def get_apy(self):
        return self.__apy

    def get_address(self):
        return self.__to_address
    
    def set_delta(self, delta):
        self.__delta = delta     
        
    def set_time_delta(self, time_delta):
        self.__t_delta = time_delta     
    
    def type_of(self):
        return TokenEvent.EVENT_SWAP