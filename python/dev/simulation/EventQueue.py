# Last in First out queue

import queue
from python.dev.helper import CopyAction

class EventQueue():
    
    def __init__(self, q = None):
        self.__queue = queue.Queue() if q == None else q
        self.__event_batches = {}
        
    def get_queue(self):
        return self.__queue
    
    def get_event(self):                
        return self.__queue.get()
    
    def get_n_events(self):
        return self.__queue.qsize()    
   
    def get_event_batches(self):
        return self.__event_batches 
      
    def add_event(self, event):
        event =  CopyAction().apply(event, True) 
        self.__queue.put(event)
        
    def reset_events(self, *events):   
        for event in events:
            event =  CopyAction().apply(event, False)
  
    def add_event_batch(self, event_batch):
        for event in event_batch: 
            self.__queue.put(event)
                 
        

            


