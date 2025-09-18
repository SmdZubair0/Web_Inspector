from lxml import etree

from src.main.schemas import Locator
from src.main.generator.base import LocatorStrategy, Runner


class XPathLocator(LocatorStrategy):

    def __init__(self, helper : Runner):
        self.generator = helper
        
    def create(self,
               element : etree._ElementTree,
               elememt_dom : etree._ElementTree) -> Locator:

        loc = {
            'type' : 'xpath',
            'locators' : []
        }

        locators = self.generator.run(element, elememt_dom)

        loc['locators'] = list(locators)
        
        return loc