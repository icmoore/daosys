import queue
from python.dev.helper import CopyAction
from python.dev.helper import ActionLog
from python.dev.event import TokenEvent

################## FIX #######################
### Must accept one time_delta per batch #####
##############################################


class ActionBatch():
    
    def __init__(self, name, n_batches = 0):
        self.__name = name
        self.__n_batches = n_batches
        self.__init = []
        self.__actions = []
        self.__t_deltas = []
        self.__instructions = {}
        self.__batch = {}
        
    def get_batch(self):
        return self.__batch  
    
    def get_actions(self):
        return self.__actions      
        
    def init_action(self, action):
        self.__init.append(action)  
        self.__set_instruction('init', self.__init)
        self.__set_instruction('n_batches', self.__n_batches)
        
    def add_action(self, action):
        self.__actions.append(action) 
        self.__set_instruction('actions', self.__actions)
        
    def generate(self):
        self.__batch['name'] = self.__name
        self.__batch['n_batches'] = self.__n_batches
        self.__batch['init'] = self.__unpack_actions(self.__init) 
        self.__batch['action'] = {}
        if(len(self.__actions) != 0):
            for k in range(self.__n_batches):
                self.__t_deltas = []
                self.__batch['action'][k] = {} 
                self.__batch['action'][k]['set'] = self.__get_next_set()
                self.__batch['action'][k]['t_delta'] = self.__t_deltas[-1]
    
        return self.__batch

    def inspect(self):        
        if(len(self.__init) != 0):    
            print('** {} INIT BATCH **'.format(self.__name))
            for action in self.__init:
                self.__event_info(action)
            if(len(self.__actions) != 0): print('\n')        
          
        if(len(self.__actions) != 0):
            print('** {} ACTION BATCH **'.format(self.__name))
            for action in self.__actions:
                self.__event_info(action)   
                self.__inspect_action(action) 
            
        self.__batch_info()  
        
    def __get_next_set(self):   
        return self.__unpack_actions(self.__actions)    
    
    def __unpack_actions(self, arr):      
        actions = []
        for action in arr:
            action = CopyAction(actions).apply(action, True)
            if(self.__inspect_action(action)): 
                actions.append(action)
        return actions 
    
    def __inspect_action(self, action):
        
        action_type = action.get_type()
        t_delta = abs(action.get_event().get_time_delta())
        #print('time delta {}'.format(action_type, t_delta))
        coin = action.get_target().get_name()
        
        if(action_type == TokenEvent.EVENT_DEPOSIT):
            self.__t_deltas.append(t_delta)
        elif(action_type == TokenEvent.EVENT_WITHDRAW and len(self.__t_deltas) == 0):
            self.__t_deltas.append(t_delta)    

        if(action_type == TokenEvent.EVENT_DEPOSIT and len(self.__t_deltas) != 0 and 
           t_delta != self.__t_deltas[-1]):
            print('Error: time delta for {} not homogenous with other deposits'.format(coin))
            return False
        
        return True    
                
    def __set_instruction(self, key, obj):
        self.__instructions[key] = obj
                                  
    def __event_info(self, action):
        ActionLog().archive(action, False)
    
    
    def __batch_info(self): 
        if(len(self.__t_deltas) != 0):
            print('\n ** REPEAT BATCH ** \n {} times'.format(self.__n_batches ))
            print('\n ** RUNTIME for 1st BATCH ** \n{} seconds'.format(self.__t_deltas[-1]))
        elif(len(self.__actions) != 0):    
            print('Error: action batch has no deposit; batch requires at least one deposit')

            
            
              
    
    

            
            
            
            
    

    
    
    