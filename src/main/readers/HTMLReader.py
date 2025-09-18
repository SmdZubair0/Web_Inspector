from pathlib import Path
from lxml import etree, html

from src.main.readers import DOMReader

class HTMLReader(DOMReader):

    def readFromFile(self, path: Path) -> etree._ElementTree:
        return html.parse(path).getroot()
    
    def readFromString(self, string: str) -> etree._ElementTree:
        element = html.fromstring(string)
        return etree.ElementTree(element).getroot()