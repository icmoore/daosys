import numpy as np

class LiquidityPoolUSD():
    
    def __init__(self, x_arr, y_arr, p_yx_arr):       
        self.x_arr = x_arr
        self.y_arr = y_arr
        self.p_yx_arr = p_yx_arr
 
    def lp_position_usd(self, x_pos, y_pos, N = None):
        if(N != None):
            usd_lp = self.usd_per_lp(N)
        else:    
            usd_lp = self.usd_per_lp()
            
        lp = self.liq(x_pos,y_pos)
        return usd_lp*lp
    
    def hodl_position_usd(self, x_pos, y_pos, N = None):
        if(N != None):
            return y_pos + self.p_yx_arr[N]*x_pos
        else:
            return y_pos + self.p_yx_arr*x_pos    

    def lp_marketcap_usd(self, N = None):
        if(N != None):
            usd_lp = self.usd_per_lp(N)
            lp = self.liq(self.x_arr[N],self.y_arr[N])
        else:    
            usd_lp = self.usd_per_lp()
            lp = self.liq()
        
        return usd_lp*lp
    
    def liq(self, x = None, y = None):
        if((x != None) and (y != None)):
            return np.sqrt(x*y) 
        else:
            return np.sqrt(self.x_arr*self.y_arr) 
        
    def lp_usd(self, N = None):
        
        if(N != None):
            return self.y_arr[N] + self.x_arr[N]*self.p_yx_arr[N]
        else:
            return self.y_arr + self.x_arr*self.p_yx_arr

    def usd_per_lp(self, N = None):
        if(N != None):
            L = self.liq(self.x_arr[N], self.y_arr[N])
            L_USD = self.lp_usd(N)
        else: 
            L = self.liq()
            L_USD = self.lp_usd() 
            
        return L_USD/L   