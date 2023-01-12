import numpy as np

from python.dev.cpt import SolveDeltas
from python.dev.math.model import TokenDeltaModel

class SimulateLiquidity():
    
    def __init__(self, liq, tdel=None, deposits=None, withdrawls=None):
        self.__liq = liq
        self.__sDel = SolveDeltas(self.__liq)
        self.__tdel_model = TokenDeltaModel() if tdel == None else tdel  
        self.__deposits = False if deposits == None else deposits
        self.__withdrawls = False if withdrawls == None else withdrawls
        self.__sys_arr = np.array([self.__liq.get_x_real()])
        self.__dai_arr = np.array([self.__liq.get_y_real()])
        self.__dsys_arr = np.array([]) 
        self.__ddai_arr = np.array([])
        self.__p_arr = None
        
    def run(self, p_arr, dx_rate = 0.5, dy_rate = 0.5):
        self.__p_arr = p_arr
        for p in p_arr[1:]:
            swap_dx, swap_dy = self.__sDel.apply(p)
            self.__sDel.apply(p) 
            self.add_deltas(dx_rate, dy_rate)
            self.update_arr(swap_dx, swap_dy)
    
    def get_liquidity_obj(self):
        return self.__liq 

    def get_sys_arr(self):
        return self.__sys_arr 

    def get_dai_arr(self):
        return self.__dai_arr
    
    def get_usd_arr(self):
        return self.__dai_arr+self.__sys_arr*self.__p_arr     
    
    def get_sys_deltas_arr(self):
        return self.__dsys_arr    
  
    def get_dai_deltas_arr(self):
        return self.__ddai_arr     
    
    def add_deltas(self, dx_rate, dy_rate):
        
        if(self.__deposits): 
            dx = self.__tdel_model.delta(dx_rate)
            self.__sDel.add_dx(dx)          
        
        if(self.__withdrawls): 
            dy = self.__tdel_model.delta(dy_rate)
            self.__sDel.add_dy(dy)         
    
    def update_arr(self, swap_dx, swap_dy):
        self.__sys_arr = np.append(self.__sys_arr,  self.__liq.get_x_real())
        self.__dai_arr = np.append(self.__dai_arr,  self.__liq.get_y_real())
        self.__dsys_arr = np.append(self.__sys_arr, swap_dx)
        self.__ddai_arr = np.append(self.__dai_arr, swap_dy)
        
    def check(self, p_arr, N):  
        p_calc_arr = abs(self.__ddai_arr/self.__dsys_arr)
        liq_arr = np.sqrt(self.__dai_arr*self.__sys_arr)

        raw_price = p_arr[N]
        yx_price = self.__dai_arr[N]/self.__sys_arr[N]
        dydx_price = p_calc_arr[N-1]
        print('raw: {:.7f} y/x: {:.7f} dy/dx: {:.7f} liq: {:.7f}'.format(raw_price, yx_price, dydx_price, liq_arr[N]))

    
    