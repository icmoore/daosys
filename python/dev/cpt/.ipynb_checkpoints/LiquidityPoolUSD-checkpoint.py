import numpy as np

class LiquidityPoolUSD():
    
    def __init__(self, x_arr, y_arr, p_yx_arr):       
        self.x_arr = x_arr
        self.y_arr = y_arr
        self.p_yx_arr = p_yx_arr
 
    def lp_position_usd(self, x_pos, y_pos, start_pt = 0, N = None):
        if(N != None):
            usd_lp = self.usd_per_lp(N)
        else:    
            usd_lp = self.usd_per_lp()
            
        lp = self.liq(x_pos,y_pos)
        return usd_lp[start_pt:]*lp
    
    def hodl_position_usd(self, x_pos, y_pos, start_pt = 0, N = None):
        if(N != None):
            return y_pos + self.p_yx_arr[N]*x_pos
        else:
            return y_pos + self.p_yx_arr[start_pt:]*x_pos    

    def lp_marketcap_usd(self, N = None):
        if(N != None):
            usd_lp = self.usd_per_lp(N)
            lp = self.liq(self.x_arr[N],self.y_arr[N])
        else:    
            usd_lp = self.usd_per_lp()
            lp = self.liq()
        
        return usd_lp*lp
    
    def lp_fee_usd(self, simLiq, N = None):
        x_fees = simLiq.get_fee_sys_arr()
        y_fees = simLiq.get_fee_dai_arr()
        if(N == None):
            collected_fees = y_fees + self.p_yx_arr[1:]*x_fees 
        else:    
            collected_fees = y_fees[N] + self.p_yx_arr[N]*x_fees[N]
            
        return collected_fees    
    
    def liq(self, x = None, y = None):
        if((x != None) and (y != None)):
            return np.sqrt(x*y) 
        else:
            return np.sqrt(self.x_arr*self.y_arr) 
        
    def lp_tot_usd(self, N = None):
        
        if(N != None):
            return self.y_arr[N] + self.x_arr[N]*self.p_yx_arr[N]
        else:
            return self.y_arr + self.x_arr*self.p_yx_arr

    def usd_per_lp(self, N = None):
        if(N != None):
            L = self.liq(self.x_arr[N], self.y_arr[N])
            L_USD = self.lp_tot_usd(N)
        else: 
            L = self.liq()
            L_USD = self.lp_tot_usd() 
            
        return L_USD/L   