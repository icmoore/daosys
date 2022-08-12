from abc import *

class TokenEvent(ABC):
    
    EVENT_DEPOSIT = 'DEPOSIT'
    EVENT_DEPOSIT_CHAIN = 'DEPOSIT_CHAIN'
    EVENT_LP_DEPOSIT_CHAIN = 'LP_DEPOSIT_CHAIN'
    EVENT_WITHDRAW = 'WITHDRAW'
    EVENT_WITHDRAW_CHAIN = 'WITHDRAW_CHAIN'
    EVENT_LP_WITHDRAW_CHAIN = 'LP_WITHDRAW_CHAIN'
    EVENT_REBASE = 'REBASE'
    EVENT_MINT = 'MINT'
    EVENT_SWAP = 'SWAP'
        
    @abstractmethod
    def get_time_delta(self, peek = False):
        pass 
    @abstractmethod
    def type_of(self):
        pass
    @abstractmethod
    def get_apy(self):
        pass
    @abstractmethod
    def get_delta(self):
        pass  
    @abstractmethod
    def set_delta(self, delta):
        pass 
    @abstractmethod
    def set_time_delta(self, time_delta):
        pass     
   
    