import numpy as np

class SimLPFees():
    
    def __init__(self, simLiq, lpVal):
        self.__sim_liq = simLiq
        self.__lp_val = lpVal
        
    def tot_fees_usd(self):
        p_arr = self.__sim_liq .get_price_arr()
        fee_sys_arr = self.__sim_liq .get_fee_x_arr()
        fee_dai_arr = self.__sim_liq .get_fee_y_arr()
        fees = fee_dai_arr + p_arr[1:]*fee_sys_arr
        return fees
        
    def position_fees_usd(self, pos_x, pos_y, start_pt = 0):
        fees = self.tot_fees_usd()
        lp_pos = self.__lp_val.lp_position_usd(pos_x, pos_y)
        lp_tot = self.__lp_val.lp_tot_usd()
        collected_fees = fees[start_pt:]*lp_pos[(start_pt+1):]/lp_tot[(start_pt+1):]
        return collected_fees
    
    def lp_position_fees_usd(self, pos_x, pos_y, start_pt = 0):
        collected_fees = self.position_fees_usd(pos_x, pos_y, start_pt)
        return np.cumsum(collected_fees)
    
    def position_percent_returns(self, pos_x, pos_y, start_pt = 0):
        lp_pos_collected_fees = self.lp_position_fees_usd(pos_x, pos_y, start_pt)
        lp_pos = self.__lp_val.lp_position_usd(pos_x, pos_y)
        return lp_pos_collected_fees/lp_pos[start_pt]