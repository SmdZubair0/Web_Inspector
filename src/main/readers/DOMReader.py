from lxml import etree
from pathlib import Path
from abc import ABC, abstractmethod


class DOMReader(ABC):
    
    @abstractmethod
    def readFromFile(self, path: Path) -> etree._ElementTree:
        pass

    @abstractmethod
    def readFromString(self, string: str) -> etree._ElementTree:
        pass