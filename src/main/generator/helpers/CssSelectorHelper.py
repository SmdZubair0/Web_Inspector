from lxml import etree
from typing import Set, List

from src.main.generator.base import *
from src.main.utils import DomExplorer


class CssSelectorHelper(Runner, SiblingExplorer, ParentExplorer, BasicSelectorProvider):

    def __init__(self):
        self.selectors = set()
        self.dom_explorer = DomExplorer()

    def run(self,
            element : etree._ElementTree,
            element_dom : etree._ElementTree) -> Set[str]:

        parents = self.dom_explorer.find_all_parents(element, element_dom)

        # basic locatos specific to element
        ele_selector = self.get_basic_selectors(element)

        direct_parent_selector = []
        direct_sibling_selector = []
        indirect_parent_selector = []
        parent_sibling_selector = []

        if parents[0] is not None:
            # locator using direct parent and element
            direct_parent_selector = self.find_parent_locator(parents[0], ele_selector)
            # locator usgin direct sibling of element
            direct_sibling_selector = self.find_sibling_locator(element, parents[0], ele_selector)
        
        if len(parents) > 1 and parents[1] is not None:
            if len(direct_parent_selector) > 0:
                # locator using indirect parent of element
                indirect_parent_selector = self.find_parent_locator(parents[1], direct_parent_selector)
                # locator using parent's sibling
                parent_sibling_selector = self.find_sibling_locator(parents[0], parents[1], direct_parent_selector)
            else :
                indirect_parent_selector = self.find_parent_locator(parents[1], ele_selector)
                parent_sibling_selector = self.find_sibling_locator(element, parents[1], ele_selector)
                
        self.selectors.update(ele_selector)
        self.selectors.update(direct_parent_selector)
        self.selectors.update(direct_sibling_selector)
        self.selectors.update(indirect_parent_selector)
        self.selectors.update(parent_sibling_selector)
        
        return self.selectors
    
    def find_parent_locator(self,
                            parent : etree._ElementTree,
                            ele_selector : List[str]) -> List[str]:
        """
            find selectors for element using its parent's locator
            - parent - parent element
            - ele_selector - elements css locators
        """
        direct_parent_selector = []
        direct_parent = self.get_basic_selectors(parent)

        # selectors using direct parents
        for i in direct_parent:
            for j in ele_selector:
                direct_parent_selector.append(f"{i} > {j}")
        
        return direct_parent_selector
    
    
    def find_sibling_locator(self,
                             element : etree._ElementTree,
                             parent : etree._ElementTree,
                             ele_selector : List[str]) -> List[str]:
        """
            find selectors for element using its parent's locator
            - parent - parent element
            - ele_selector - elements css locators
        """

        direct_sibling_selectors = []
        
        direct_sibling = self.dom_explorer.get_siblings(parent, element)
        if len(direct_sibling) == 0:
            return direct_sibling_selectors
        
        direct_sibling_locator = []        
        if "following" in direct_sibling:
            direct_sibling_locator = self.get_basic_selectors(direct_sibling["following"])


        # select direct sibling locator
        for i in direct_sibling_locator:
            for j in ele_selector:
                direct_sibling_selectors.append(f"{i} + {j}")
        
        return direct_sibling_selectors

    
    def get_basic_selectors(self, el : etree._ElementTree) -> List[str]:
        """
        Generate basic CSS selectors for an element:
        - id
        - class (single + combinations)
        - tag + class
        - attributes like name, type, aria-label, alt
        """
        tag = el.tag
        selectors = [tag]

        # ID selector
        for id in (el.attrib.get('id') or "").split():
            if id[0].isdigit():
                id = f"#\\3{id[0]} " + id[1:]
            selectors.append(f"{tag}#{id}")   # tag + id

        # Class selectors single
        classes = (el.attrib.get('class') or "").split()

        # Single class
        for c in classes:
            selectors.append(f".{c}")
            selectors.append(f"{tag}.{c}")

        # Attribute selectors (common ones)
        for attr in ['name', 'type', 'value', 'placeholder', 'aria-label', 'alt', 'title', 'role']:
            if attr in el.attrib and el.attrib[attr].strip():
                selectors.append(f"[{attr}=\"{el.attrib[attr]}\"]")
                selectors.append(f"{tag}[{attr}=\"{el.attrib[attr]}\"]")

        return selectors
