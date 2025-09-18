from lxml import etree
from typing import List
from abc import ABC, abstractmethod

class BasicSelectorProvider(ABC):

    @abstractmethod
    def get_basic_selectors(self, el : etree._ElementTree) -> List[str]:
        pass