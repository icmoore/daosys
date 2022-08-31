from python.dev.event import TokenEvent

class ActionLog():
    
    def __init__(self, verbose = True):
        self.__verbose = verbose
        self.__a_log = {}
    
    def archive(self, action, show_delta = True):
        index = self.__log_index()
        self.log_action(action, index, show_delta)
        if(self.__verbose): self.print_index(index, show_delta)  

    def log_action(self, action, index, show_delta = True):
        action_type = action.get_type() 
        if(action_type == TokenEvent.EVENT_MINT):
            self.__mint(action, index, show_delta)
        elif(action_type == TokenEvent.EVENT_DEPOSIT or action_type == TokenEvent.EVENT_WITHDRAW):    
            self.__deposit_withdraw(action, index, show_delta) 
        elif(action_type == TokenEvent.EVENT_SWAP):    
            self.__swap(action, index, show_delta)
        elif(action_type == TokenEvent.EVENT_WITHDRAW_CHAIN):    
            self.__withdraw_chain(action, index, show_delta)  
        elif(action_type == TokenEvent.EVENT_LP_DEPOSIT_CHAIN):  
            self.__lp_deposit_chain(action, index, show_delta)  
        
    def print_logs(self, user = None):
        print('======== Log Events ===========')
        print('# num_events: {} \n'.format(len(self.__a_log)))          
        
        user_name = None if user == None else user.get_name() 
        for index in self.__a_log:    
            if(user_name == None):
                self.print_index(index, True)
            elif(user_name == self.__a_log[index]['user']): 
                self.print_index(index, True)
               
    def print_index(self, index, show_delta):
        action_type = self.__a_log[index]['action_type'] 
        if(action_type == TokenEvent.EVENT_MINT):
            self.__print_mint(index, show_delta)
        elif(action_type == TokenEvent.EVENT_DEPOSIT or action_type == TokenEvent.EVENT_WITHDRAW):    
            self.__print_deposit_withdraw(index, show_delta) 
        elif(action_type == TokenEvent.EVENT_SWAP):    
            self.__print_swap(index, show_delta)
        elif(action_type == TokenEvent.EVENT_WITHDRAW_CHAIN):     
            self.__print_withdraw_chain(index, show_delta)  
        elif(action_type == TokenEvent.EVENT_LP_DEPOSIT_CHAIN):  
            self.__print_lp_deposit_chain(index, show_delta) 
                   
    def get_logs(self):
        return self.__a_log
    
    def __get_current_banlance(self, action):
        token_agent = action.get_target()
        mint_id = action.get_mint_id()
        addresses = token_agent.get_addresses()
        address = None if len(addresses) == 0 else token_agent.get_address(mint_id)    
        balance = 0 if address == None else token_agent.get_token().get_balance_deposits([address])      
        return balance
     
    def __log_index(self):
        index = len(self.__a_log) 
        self.__a_log[index] = {}
        return index   

    def __mint(self, action, index, show_delta):       
        self.__a_log[index]['coin'] = action.get_target().get_name()
        self.__a_log[index]['delta'] = abs(action.get_event().get_delta())
        self.__a_log[index]['user'] = action.get_user().get_name()
        self.__a_log[index]['action_type'] = action.get_type()
        self.__a_log[index]['coin_balance'] = self.__get_current_banlance(action)
        

    def __deposit_withdraw(self, action, index, show_delta): 
        self.__a_log[index]['coin'] = action.get_target().get_name()
        self.__a_log[index]['delta'] = abs(action.get_event().get_delta())
        self.__a_log[index]['user'] = action.get_user().get_name()
        self.__a_log[index]['action_type'] = action.get_type()   
        self.__a_log[index]['coin_balance'] = self.__get_current_banlance(action)
        
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            self.__a_log[index]['t_stamp'] = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
                            
    def __swap(self, action, index, show_delta):
        self.__a_log[index]['user'] = action.get_user().get_name()
        self.__a_log[index]['action_type'] = action.get_type()
        self.__a_log[index]['from_coin'] = action.get_target('WITHDRAW').get_name()
        self.__a_log[index]['to_coin'] = action.get_target('DEPOSIT').get_name()
        self.__a_log[index]['delta'] = abs(action.get_event().get_delta())    
        self.__a_log[index]['coin_balance'] = self.__get_current_banlance(action)
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            self.__a_log[index]['t_stamp'] = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")       
        
    def __withdraw_chain(self, action, index, show_delta):
        self.__a_log[index]['coin'] = action.get_target().get_name()
        self.__a_log[index]['user'] = action.get_user().get_name()
        self.__a_log[index]['action_type'] = action.get_type()
        self.__a_log[index]['delta'] = abs(action.get_event().get_delta())
        self.__a_log[index]['coin_balance'] = self.__get_current_banlance(action)
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            self.__a_log[index]['t_stamp'] = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
            
    def __lp_deposit_chain(self, action, index, show_delta):
        self.__a_log[index]['lp'] = action.get_target().get_name()
        self.__a_log[index]['user'] = action.get_user().get_name()
        self.__a_log[index]['action_type'] = action.get_type()
        self.__a_log[index]['coin1'] = action.get_action1().get_target().get_name()
        self.__a_log[index]['coin2'] = action.get_action2().get_target().get_name()
        self.__a_log[index]['delta'] = abs(action.get_event().get_delta())
        self.__a_log[index]['coin_balance'] = self.__get_current_banlance(action)
        if(show_delta):
            clock = action.get_target().get_token().get_clock()
            self.__a_log[index]['t_stamp'] = clock.get_time_stamp().strftime("%Y-%m-%d %H:%M:%S")
        
    def __print_mint(self, index, show_delta): 
        print('{} {}s {:.2f} {} '.format(self.__a_log[index]['user'], 
                                         self.__a_log[index]['action_type'], 
                                         self.__a_log[index]['delta'], 
                                         self.__a_log[index]['coin'])) 
        
    def __print_deposit_withdraw(self, index, show_delta): 
        if(show_delta):
            print('[{}] {} {}s {:.2f} {} [{:.0f} TOTAL TOKEN]'.format(self.__a_log[index]['t_stamp'], 
                                                 self.__a_log[index]['user'], 
                                                 self.__a_log[index]['action_type'], 
                                                 self.__a_log[index]['delta'], 
                                                 self.__a_log[index]['coin'],
                                                 self.__a_log[index]['coin_balance'])) 
        else: 
            print('{} {}s {} '.format(self.__a_log[index]['user'],
                                      self.__a_log[index]['action_type'], 
                                       self.__a_log[index]['coin']))  
            
    def __print_swap(self, index, show_delta): 
        if(show_delta):
            print('[{}] {} {}s {:.2f} {} for {}'.format(self.__a_log[index]['t_stamp'], 
                                                        self.__a_log[index]['user'], 
                                                        self.__a_log[index]['action_type'], 
                                                        self.__a_log[index]['delta'], 
                                                        self.__a_log[index]['from_coin'], 
                                                        self.__a_log[index]['to_coin']))
        else:
            print('{} {}s {} for {} '.format(self.__a_log[index]['user'], 
                                             self.__a_log[index]['action_type'], 
                                             self.__a_log[index]['from_coin'], 
                                             self.__a_log[index]['to_coin']))             
        
    def __print_withdraw_chain(self, index, show_delta): 
        if(show_delta):
            print('[{}] {} WITHDRAWs {:.2f} from {} proceeds'.format(self.__a_log[index]['t_stamp'], 
                                                                     self.__a_log[index]['user'], 
                                                                     self.__a_log[index]['delta'],
                                                                     self.__a_log[index]['coin']))
        else:
            print('{} WITHDRAWs {} proceeds'.format(self.__a_log[index]['user'], 
                                                    self.__a_log[index]['coin'])) 
            
    def __print_lp_deposit_chain(self, index, show_delta): 
        if(show_delta):
            print('[{}] {} DEPOSITs {:.2f} {} from {} and {} proceeds [{:.0f} TOTAL LP]'.format(self.__a_log[index]['t_stamp'], 
                                                                              self.__a_log[index]['user'], 
                                                                              self.__a_log[index]['delta'], 
                                                                              self.__a_log[index]['lp'], 
                                                                              self.__a_log[index]['coin1'], 
                                                                              self.__a_log[index]['coin2'],
                                                                              self.__a_log[index]['coin_balance']))
        else:
            print('{} DEPOSITs {} and {} proceeds into {}'.format(self.__a_log[index]['user'], 
                                                                  self.__a_log[index]['coin1'], 
                                                                  self.__a_log[index]['coin2'], 
                                                                  self.__a_log[index]['lp']))                
             
                   