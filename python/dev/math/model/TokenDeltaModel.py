import numpy as np
from python.dev.math.model import EventSelectionModel
  
MAX_TRADE = 10000    
    
class TokenDeltaModel():
    
    def __init__(self, shape=1, scale=1):
        self.__shape = shape
        self.__scale = scale

    def apply(self, n = 1, max_trade = 10000):
        
        if(n == 1):
            rval = self.delta(self, max_trade)
            return min(rval, max_trade)  
        else:
    
            res = []
            for k in range(n):
                rval = self.delta(self, max_trade)
                res.append(min(rval,max_trade))
                
            return res  
        
    def delta(self, p=1, max_trade=100):
        self.__scale = max_trade/5
        return self.add_sub(p)*np.random.gamma(self.__shape, self.__scale)   
    
    def add_sub(self, p):
        return 1 if bool(EventSelectionModel().bi_select(p)) else -1     