import numpy as np

from python.dev.cpt import SolveDeltas
from python.dev.math.model import TokenDeltaModel

class SimulateLiquidity():
    
    def __init__(self, liq, tdel=None):
        self.__liq = liq
        self.__sDel = SolveDeltas(self.__liq)
        self.__tdel_model = TokenDeltaModel() if tdel == None else tdel  
        self.__x_arr = np.array([self.__liq.get_x_real()])
        self.__y_arr = np.array([self.__liq.get_y_real()])
        self.__dx_arr = np.array([]) 
        self.__dy_arr = np.array([])
        self.__fee_x_arr = np.array([]) 
        self.__fee_y_arr = np.array([])        
        self.__p_arr = None
        self.__x_fee = 0       
        self.__y_fee = 0 
        
    def run(self, p_arr, lp_rate = 0.5):
        self.__p_arr = p_arr
        for p in p_arr[1:]:
            swap_dx, swap_dy = self.__sDel.apply(p)
            self.update_fees(self.__sDel.get_x_fee(), self.__sDel.get_y_fee())
            if(lp_rate > 0.54): self.add_lp_delta(p, lp_rate)
            self.update_arr(swap_dx, swap_dy)
            self.reset_fees()
            
    def add_lp_delta(self, p, lp_rate):
        dx = self.__tdel_model.delta(lp_rate)
        dy = p*dx   
        self.__sDel.add_dx(dx)
        self.__sDel.add_dy(dy) 
        
        if(dx < 0): 
            self.__liq.swap(dx, -dy)
            self.update_fees(self.__liq.get_x_fee(), self.__liq.get_y_fee())
    
    def get_liquidity_obj(self):
        return self.__liq 

    def get_x_arr(self):
        return self.__x_arr 

    def get_y_arr(self):
        return self.__y_arr
    
    def get_fee_x_arr(self):
        return self.__fee_x_arr

    def get_fee_y_arr(self):
        return self.__fee_y_arr 
    
    def get_price_arr(self):
        return self.__p_arr     
    
    def get_usd_arr(self):
        return self.__y_arr+self.__x_arr*self.__p_arr     
    
    def get_x_deltas_arr(self):
        return self.__dx_arr    
  
    def get_y_deltas_arr(self):
        return self.__dy_arr     
    
    def update_fees(self, x_fee, y_fee):
        self.__x_fee += x_fee      
        self.__y_fee += y_fee
        
    def reset_fees(self):
        self.__x_fee = 0       
        self.__y_fee = 0 
    
    def update_arr(self, swap_dx, swap_dy):
        self.__x_arr = np.append(self.__x_arr,  self.__liq.get_x_real())
        self.__y_arr = np.append(self.__y_arr,  self.__liq.get_y_real())
        self.__dx_arr = np.append(self.__x_arr, swap_dx)
        self.__dy_arr = np.append(self.__y_arr, swap_dy)
        self.__fee_x_arr = np.append(self.__fee_x_arr, self.__x_fee)
        self.__fee_y_arr = np.append(self.__fee_y_arr, self.__y_fee)        
        
    def check(self, p_arr, N):  
        p_calc_arr = abs(self.__dy_arr/self.__dx_arr)
        liq_arr = np.sqrt(self.__y_arr*self.__x_arr)

        raw_price = p_arr[N]
        yx_price = self.__y_arr[N]/self.__x_arr[N]
        dydx_price = p_calc_arr[N-1]
        print('raw: {:.7f} y/x: {:.7f} dy/dx: {:.7f} liq: {:.7f}'.format(raw_price, yx_price, dydx_price, liq_arr[N]))

    
    