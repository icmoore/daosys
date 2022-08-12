from python.dev.event import TokenEvent
import uuid

class Mint(TokenEvent):
    
    TYPE_REBASE = 'REBASE'
    TYPE_NONREBASE = 'NONREBASE'      
        
    def __init__(self, delta, apy, is_rebase):
        self.__delta = delta
        self.__apy = apy
        self.__is_rebase = is_rebase
        self.__mint_id = uuid.uuid4().int
        self.__t_delta = 0
        
        
    def get_apy(self):
        return self.__apy
    
    def get_delta(self):
        return self.__delta   
    
    def get_time_delta(self):
        return self.__t_delta
    
    def get_id(self):
        return self.__mint_id  
    
    def set_delta(self, delta):
        self.__delta = delta     
        
    def set_time_delta(self, time_delta):
        self.__t_delta = time_delta     
    
    def type_of(self):
        return TokenEvent.EVENT_MINT
    
    def get_token_type(self):
        if(self.__is_rebase):
            return self.TYPE_REBASE
        else: 
            return self.TYPE_NONREBASE