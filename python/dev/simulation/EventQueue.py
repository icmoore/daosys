# Last in First out queue

import queue
from python.dev.simulation.batch import MergeBatch
from python.dev.helper import CopyAction

class EventQueue():
    
    def __init__(self, q = None):
        self.__queue = queue.Queue() if q == None else q
        self.__mb = MergeBatch('MERGED_ACTIONS')
        self.__all_batches = {}
        
    def get_queue(self):
        return self.__queue
    
    def get_all_batches(self):
        return  self.__all_batches   
    
    def get_event(self):                
        return self.__queue.get()
    
    def get_n_events(self):
        return self.__queue.qsize()    
   
    def get_event_batches(self):
        return self.__event_batches 
      
    def add_event(self, event):
        event =  CopyAction().apply(event, False) 
        self.__queue.put(event)
    
    def add_setup_batch(self, event_batch):
        batch_name = event_batch['name']
        setup_events = event_batch['init']   
        n_batches = event_batch['n_batches']
        self.__all_batches[batch_name] = event_batch
        
        for event in setup_events: 
            self.__queue.put(event)                    
           
    def add_action_batch(self, input_batch):
        self.__mb.add(input_batch)
        
    def freeze(self):
        event_batch = self.__mb.merge()
        batch_name = event_batch['name'] 
        action_batch = event_batch['action']
        n_batches = event_batch['n_batches']
        self.__all_batches[batch_name] = event_batch

        for k in range(n_batches):
            for event in action_batch[k]['set']: 
                self.__queue.put(event)
        

            
                 
        

            


