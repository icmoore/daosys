
class ActionInfo():
    
    def printout(self, action, show_delta = True):
        action_type = action.get_type()
        
        if(action_type == 'MINT'):
            self.__mint(action, show_delta)
        elif(action_type == 'DEPOSIT' or action_type == 'WITHDRAW'):    
            self.__deposit_withdraw(action, show_delta) 
        elif(action_type == 'SWAP'):    
            self.__swap(action, show_delta)
        elif(action_type == 'WITHDRAW_CHAIN'):    
            self.__withdraw_chain(action, show_delta)  
        elif(action_type == 'LP_DEPOSIT_CHAIN'):  
            self.__lp_deposit_chain(action, show_delta) 
    
    def __mint(self, action, show_delta):
        coin = action.get_target().get_name()
        delta = abs(action.get_event().get_delta())
        user = action.get_user().get_name()
        action_type = action.get_type()
        print('{} {}s {:.2f} {} '.format(user, action_type, delta, coin)) 
    
    def __deposit_withdraw(self, action, show_delta): 
        
        coin = action.get_target().get_name()
        delta = abs(action.get_event().get_delta())
        user = action.get_user().get_name()
        action_type = action.get_type()   
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            t_stamp = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
            #t_stamp = abs(action.get_event().get_time_delta())
            print('[{}] {} {}s {:.2f} {}'.format(t_stamp, user, action_type, delta, coin)) 
        else: 
            print('{} {}s {} '.format(user, action_type, coin))
            
    def __swap(self, action, show_delta):
        user = action.get_user().get_name()
        action_type = action.get_type()
        from_coin = action.get_target('WITHDRAW').get_name()
        to_coin = action.get_target('DEPOSIT').get_name()
        delta = abs(action.get_event().get_delta())        
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            t_stamp = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
            #t_stamp = abs(action.get_event().get_time_delta())
            print('[{}] {} {}s {:.2f} {} for {}'.format(t_stamp, user, action_type, delta, from_coin, to_coin))
        else:
            print('{} {}s {} for {} '.format(user, action_type, from_coin, to_coin))
            
        
    def __withdraw_chain(self, action, show_delta):
        coin = action.get_target().get_name()
        user = action.get_user().get_name()
        action_type = action.get_type()
        delta = abs(action.get_event().get_delta())
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            t_stamp = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
            #t_stamp = abs(action.get_event().get_time_delta())
            print('[{}] {} WITHDRAWs {:.2f} from {} proceeds'.format(t_stamp, user, delta, coin))
        else:
            print('{} WITHDRAWs {} proceeds'.format(user, coin))
            
        
    def __lp_deposit_chain(self, action, show_delta):
        lp = action.get_target().get_name()
        user = action.get_user().get_name()
        action_type = action.get_type()
        coin1 = action.get_action1().get_target().get_name()
        coin2 = action.get_action2().get_target().get_name()
        delta = abs(action.get_event().get_delta())
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            t_stamp = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
            #t_stamp = abs(action.get_event().get_time_delta())
            print('[{}] {} DEPOSITs {:.2f} {} from {} and {} proceeds'.format(t_stamp, user, delta, lp, coin1, coin2))
        else:
            print('{} DEPOSITs {} and {} proceeds into {}'.format(user, coin1, coin2, lp))
             
                   