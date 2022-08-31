from python.dev.token import RebaseToken
from python.dev.token import NonRebaseToken
from python.dev.action import Action
from python.dev.event import Mint
from python.dev.agent import Agent
from python.dev.event import TokenEvent


class  MintAction(Action):
    
    def __init__(self, token_event, target, user, start_time = None):
        self.__token_event = token_event
        self.__target = target
        self.__user = user
        self.__mint_id = token_event.get_id()
        self.__start_time = start_time
              
    def apply(self, agents):
        
        token_type = self.__token_event.get_token_type()
        token_deposit = self.__token_event.get_delta()
        mint_id = self.__token_event.get_id()
        token_name = self.__target.get_name()
        token = self.__target.get_token()
        
        if(token_type == Mint.TYPE_REBASE):
            token = RebaseToken(token_name, self.__start_time) if token == None else token
            address = token.mint(token_deposit, 0.1) 
        elif(token_type == Mint.TYPE_NONREBASE):
            token = NonRebaseToken(token_name, self.__start_time) if token == None else token  
            address = token.mint(token_deposit)
        
        self.__target.add_address(mint_id, address)
        self.__target.set_token(token)
        self.__target.set_token_type(token_type)
                
        return True
    
    def get_event(self):
        return self.__token_event    
        
    def get_user(self):
        return self.__user
    
    def get_target(self):
        return self.__target    
        
    def get_mint_id(self):
        return self.__mint_id          
        
    def get_type(self):
        return TokenEvent.EVENT_MINT
    
    
        