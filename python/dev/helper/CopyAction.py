from python.dev.event import TokenEvent
from python.dev.event import Deposit
from python.dev.event import Withdraw
from python.dev.action import DepositAction
from python.dev.action import WithdrawAction
from python.dev.action import LPDepositChainAction

class CopyAction():
    
        
        def apply(self, action, peek = False):
            return self.__copy(action, peek)
        
        def __copy(self, action, peek):
            if(type(action) == DepositAction):
                action = self.__copy_deposit_action(action, peek) 
            elif(type(action) == WithdrawAction):
                action = self.__copy_withdraw_action(action, peek)     
            elif(type(action) == LPDepositChainAction):
                action = self.__copy_lp_deposit_action(action) 
                
            return action   
                
        
        def __copy_deposit_action(self, action, peek = False):        
        
            delta = action.get_event().get_delta(peek)
            time_delta = action.get_event().get_time_delta(peek)
            apy = action.get_event().get_apy(peek)
            
            event = Deposit(apy, delta, time_delta) 
            
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id()
            
            return DepositAction(event, target, user, mint_id)
        
        def __copy_withdraw_action(self, action, peek = False): 
                    
            delta = -action.get_event().get_delta(peek)
            time_delta = action.get_event().get_time_delta(peek)
            apy = action.get_event().get_apy(peek)
            address = action.get_event().get_address()
            
            event = Withdraw(apy, delta, time_delta, address) 
            
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id()
             
            return WithdrawAction(event, target, user, mint_id)        
        
        def __copy_lp_deposit_action(self, action): 
                    

            action1 = self.__copy(action.get_action1(), True)
            action2 = self.__copy(action.get_action2(), True)
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id()
             
            return LPDepositChainAction(action1, action2, target, user, mint_id)       
        
