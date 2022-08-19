from queue import PriorityQueue
import numpy as np

class MergeBatch():
    
    def __init__(self, name):
        self.__name = name
        self.__pq = PriorityQueue()
        self.__len = 0
        self.__n_action_batches = 0
        self.__batches = {}
        self.__merge = {}
        
    def get_n_action_batches(self): 
        return self.__n_action_batches
     
    def add(self, batch):
        arr = self.get_time(batch)
        batch_name = batch['name']
        self.add_queue(arr, batch_name)
        self.__batches[batch_name] = batch['action']
        self.__merge['name'] = self.__name
        self.__merge['n_batches'] = self.__len
        self.__n_action_batches += 1
    
    def add_queue(self, arr, arr_name):
        N = len(arr)
        self.__len += N
        for i in range(N):
            self.__pq.put([arr[i], arr_name, i]) 
            
    def get_time(self, batch):
        t_deltas = np.array([])
        for item in batch['action']: 
            val = batch['action'][item]['t_delta']
            if(len(t_deltas) != 0):
                val=val+t_deltas[-1] 
            t_deltas = np.append(t_deltas, val)      
        return t_deltas  
                         
    def gen(self):    
        j = 0
        res = [0 for i in range(self.__len)]
        while not self.__pq.empty():
            res[j] = self.__pq.get()
            j += 1 
        return  np.array(res) 
    
    def merge(self): 
        res = self.gen()
        self.__merge['init'] = {}
        self.__merge['action'] = {}
        for k in range(len(res)):
            self.__merge['action'][k] = {}
            name = res[k,1]
            index = int(res[k,2])
            self.__merge['action'][k] = self.__batches[name][index]
           
        return self.__merge       