from python.dev.event import TokenEvent
from python.dev.event import Deposit
from python.dev.event import Withdraw
from python.dev.action import DepositAction
from python.dev.action import WithdrawAction
from python.dev.action import LPDepositChainAction
from python.dev.action import WithdrawChainAction
from python.dev.action import SwapAction

class CopyAction():
    
    
        def __init__(self, prev_actions = []):
            self.__prev_actions = prev_actions
        
        def apply(self, action, reset = True):
            return self.__copy(action, reset)
        
        def __copy(self, action, reset):
            if(type(action) == DepositAction):
                action = self.__copy_deposit_action(action, reset) 
            elif(type(action) == WithdrawAction):
                action = self.__copy_withdraw_action(action, reset)     
            elif(type(action) == LPDepositChainAction and len(self.__prev_actions) > 0):
                action = self.__copy_lp_deposit_action(action, reset)
            elif(type(action) == SwapAction and len(self.__prev_actions) > 0):
                action = self.__copy_swap_action(action, reset)     
            elif(type(action) == WithdrawChainAction and len(self.__prev_actions) > 0):
                action = self.__copy_withdraw_chain_action(action, reset)                
                                              
            return action   
                
        
        def __copy_deposit_action(self, action, reset = True):        
        
            delta = action.get_event().get_delta(reset)
            time_delta = action.get_event().get_time_delta(reset)
            apy = action.get_event().get_apy(reset)
            event = Deposit(apy, delta, time_delta) 
            
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id()  
            action = DepositAction(event, target, user, mint_id)
            time_delta = action.get_event().get_time_delta()
            return action
        
        def __copy_withdraw_action(self, action, reset = True): 
                    
            delta = -action.get_event().get_delta(reset)
            time_delta = action.get_event().get_time_delta(reset)
            apy = action.get_event().get_apy(reset)
            address = action.get_event().get_address()
            event = Withdraw(apy, delta, time_delta, address) 
            
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id() 
            return WithdrawAction(event, target, user, mint_id)        
         
        def __copy_swap_action(self, action, reset): 

            action1 = self.__copy(action.get_action1(), reset)
            action2 = self.__copy(action.get_action2(), reset)             
            return SwapAction(action1, action2)           
        
        def __copy_withdraw_chain_action(self, action, reset): 

            action = self.__prev_actions[-1]            
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id()             
            return WithdrawChainAction(action, target, user, mint_id)  
        
        def __copy_lp_deposit_action(self, action, reset): 
         
            action1 = self.__prev_actions[-1]
            action2 = self.__prev_actions[-2]
            target = action.get_target()
            user = action.get_user()
            mint_id = action.get_mint_id()         
            return LPDepositChainAction(action1, action2, target, user, mint_id)            
     
        
