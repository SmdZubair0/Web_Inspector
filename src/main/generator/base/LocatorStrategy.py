from lxml import etree
from abc import ABC, abstractmethod

from src.main.schemas import Locator

class LocatorStrategy(ABC):
    @abstractmethod
    def create(self,
               element : etree._ElementTree,
               element_dom : etree._ElementTree) -> Locator:
        pass