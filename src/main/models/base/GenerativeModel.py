from abc import ABC, abstractmethod

class GenerativeModel(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def invoke(self, prompt):
        pass