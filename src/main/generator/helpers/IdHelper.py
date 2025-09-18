from lxml import etree
from typing import Set

from src.main.generator.base import Runner

class IdHelper(Runner):

    def __init__(self):
        self.selector = set()
    
    def run(self,
            element : etree._ElementTree,
            element_dom : etree._ElementTree) -> Set[str]:

        loc = []

        for id in element.attrib.get('id', "").split():
            loc.append(id)
        
        self.selector.update(loc)

        return self.selector