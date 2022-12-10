from abc import *

class OptFeature(ABC):
             
    @abstractmethod        
    def apply(self, arr):
        pass