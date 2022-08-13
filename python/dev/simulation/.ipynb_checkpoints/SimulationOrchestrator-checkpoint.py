from python.dev.event import TokenEvent
from python.dev.lp.event import MintLPEvent
from python.dev.lp.event import DepositLPEvent
from python.dev.lp.event import SwapLPEvent

from python.dev.event import Deposit
from python.dev.action import DepositAction
from python.dev.helper import CopyAction
from python.dev.helper import ActionInfo
import queue


class SimulationOrchestrator():
    
    def __init__(self, verbose = False):
        self.__agents = {}
        self.__verbose = verbose
        self.__mint_queue = queue.Queue()
        
    def get_verbose(self):
        return self.__verbose
         
    def apply(self, action):    
        is_complete = action.apply(self.__agents)  
        if(self.__verbose): self.__print_out(action)
        
        return is_complete
         
    def add_agent(self, target):
        self.__agents[target.get_name()] = target 

    def __print_out(self, action):
        ActionInfo().printout(action)
       
        