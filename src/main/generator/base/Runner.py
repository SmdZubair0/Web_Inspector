from lxml import etree
from typing import Set
from abc import ABC, abstractmethod

class Runner(ABC):
    
    @abstractmethod
    def run(self,
            element : etree.ElementTree,
            element_dom : etree.ElementTree) -> Set[str]:
        pass
