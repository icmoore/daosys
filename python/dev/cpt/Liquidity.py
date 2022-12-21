# Based on Uniswap v1 and v2 (see Reference 1); for Uniswap v3 see reference 2

# References: 

# [1] Pandichef, A Brief History of Uniswap and Its Math 
# Link: https://pandichef.medium.com/a-brief-history-of-uniswap-and-its-math-90443241c9b7

# [2] Atis Elsts, Liquidity Math in Uniswap V3  
# Link: https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf

import numpy as np
import copy

class Liquidity():
    
    YX_PRICE = 'YX'
    XY_PRICE = 'XY'
    
    def __init__(self, x_real, y_real, x_name, y_name):
        self.__x_real = x_real
        self.__y_real = y_real  
        self.__x_name = x_name
        self.__y_name = y_name        
        self.__liquidity_val = 0
        self.__yx_price = None 
        self.__x_delta = 0
        self.__y_delta = 0           
       
    def get_x_real(self):
        return self.__x_real

    def get_y_real(self):
        return self.__y_real
    
    def get_x_name(self):
        return self.__x_name  
    
    def get_y_name(self):
        return self.__y_name      
    
    def get_liquidity_val(self):
        return self.__liquidity_val  
      
    def get_price(self, direction = 'YX'): 
        
        if(self.__yx_price == None):
            self.calc()    
            
        if direction == self.YX_PRICE:
            return self.__yx_price
        else: 
            return 1/self.__yx_price    
          
    def set_y_real(self, y_real):
        self.__y_real = y_real
        
    def set_x_real(self, x_real):
        self.__x_real = x_real
        
    def set_x_name(self, x_name):
        self.__x_name = x_name  
    
    def set_y_name(self, y_name):
        self.__y_name = y_name   
        
    def add_delta_x(self, x_delta):
        self.__x_delta = x_delta
        self.__x_real = self.__x_real + x_delta  
        
    def add_delta_y(self, y_delta):
        self.__y_delta = y_delta
        self.__y_real = self.__y_real + y_delta       
        
    def calc(self): 
        
        self.__prev_liquidity_val = copy.copy(self.__liquidity_val)
        if(self.__x_real != 0):
            self.__liquidity_val = np.sqrt(self.__x_real*self.__y_real)
            self.__yx_price = self.calc_price()

        return self.__liquidity_val
    
    def calc_price(self): 
        if(self.__liquidity_val == 0):
            return 0
        else:
            return self.__y_real**2/self.__liquidity_val**2
         
    def swap(self, x_delta):
        
        #delta_y = self.calc_delta_y(delta_x)
        self.__yx_price = self.calc_price()
        self.__x_real = (self.__x_real+x_delta)
        self.__y_real = (self.__y_real-y_delta)      
         
        return np.sqrt(self.__x_real*self.__y_real)