from python.dev.helper import ActionLog
import queue


class SimulationOrchestrator():
    
    def __init__(self, verbose = False):
        self.__agents = {}
        self.__verbose = verbose
        self.__mint_queue = queue.Queue()
        self.__a_log = ActionLog(verbose)
        
    def get_verbose(self):
        return self.__verbose
    
    def get_batch_logs(self):
        return self.__a_log.get_logs()    
    
    def print_logs(self, user_name = None):
        self.__a_log.print_logs(user_name)    
         
    def apply(self, action):    
        is_complete = action.apply(self.__agents)  
        self.__a_log.archive(action)
        
        return is_complete
         
    def add_agent(self, target):
        self.__agents[target.get_name()] = target 

        
        

       
        