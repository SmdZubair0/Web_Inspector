from lxml import etree
from typing import List, Dict
from lxml.cssselect import CSSSelector

class ValidateLocator:

    def __init__(self, dom : etree._ElementTree):
        self.dom = dom
        self.final_locators = {}

    @property
    def get_locators(self) -> Dict[str, List[str]]:
        return self.final_locators
    
    def is_valid_id(self, id : str) -> bool:
        try:
            els = self.dom.xpath(f"//*[@id='{id}]")
            return len(els) == 1
        except Exception as e:
            print(f"Error with id {id} : {e}")

    def is_valid_cssSelector(self, cssSelector : str) -> bool:
        try:
            sel = CSSSelector(cssSelector)
            root = self.dom.getroottree() if hasattr(self.dom, "getroottree") else self.dom
            els = sel(root)

            return len(els) == 1
        except Exception as e:
            print(f"Error with cssSelector {cssSelector} : {e}")

    def is_valid_xpath(self, xpath) -> bool:
        try:
            els = self.dom.xpath(xpath)
            return len(els) == 1
        except Exception as e:
            print(f"Error with xpath {xpath} : {e}")


    def validate_all_locators(self, locators : List[Dict[str, List[str]]]) -> List[str]:

        for i in locators:

            type = i['type']

            self.final_locators[type] = []

            for j in i['locators']:
                
                if type == 'id':
                    if self.is_valid_id(j):
                        self.final_locators[type].append(j)
                
                elif type == 'cssSelector':
                    if self.is_valid_cssSelector(j):
                        self.final_locators[type].append(j)

                elif type == 'xpath':
                    if self.is_valid_xpath(j):
                        self.final_locators[type].append(j)
        
        self.final_locators = [{k : sorted(v, key=len)[:5]} for k, v in self.final_locators.items()]