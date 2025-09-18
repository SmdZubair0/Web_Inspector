from lxml import etree
from pathlib import Path

from src.main.readers.DOMReader import DOMReader

class XMLReader(DOMReader):
    
    def readFromFile(self, path: Path) -> etree._ElementTree:
        return etree.parse(path).getroot()
    
    def readFromString(self, string: str) -> etree._ElementTree:
        element = etree.fromstring(string)
        return etree.ElementTree(element)
