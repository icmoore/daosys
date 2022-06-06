from python.dev.agent import TokenAgent

class LPTokenAgent(TokenAgent):
      
    def __init__(self, agent_name, lp):
        super().__init__(agent_name) 
        self.__lp = lp 
        self.__lp_val = None

    def get_x_target(self):
        return self.__lp.get_x_target()         
        
    def get_y_target(self):
        return self.__lp.get_x_target()      

    def get_lp(self):
        return self.__lp     
    
    def get_lp_val(self):
        return self.__lp_val    
    
    def get_type(self):
        return Agent.TYPE_LP_TOKEN   
    
    def set_lp(self, lp):
        self.__lp = lp
        
    def set_lp_val(self, lp_val):
        self.__lp_val = lp_val        
        
  
    