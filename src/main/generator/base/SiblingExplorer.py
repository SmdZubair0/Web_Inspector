from lxml import etree
from typing import List
from abc import ABC, abstractmethod

class SiblingExplorer(ABC):
    
    @abstractmethod
    def find_sibling_locator(self,
                             element : etree._ElementTree,
                             parent : etree._ElementTree,
                             ele_selector : List[str]):
        pass

