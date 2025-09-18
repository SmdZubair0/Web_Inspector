from lxml import etree
from typing import Set, List

from src.main.generator.base import *
from src.main.utils import DomExplorer


class XPathHelper(Runner, ParentExplorer, SiblingExplorer, BasicSelectorProvider):

    def __init__(self):
        self.selectors = set()
        self.dom_explorer = DomExplorer()

    def run(self,
            element : etree._ElementTree,
            element_dom : etree._ElementTree) -> Set[str]:
        
        parents = self.dom_explorer.find_all_parents(element, element_dom)

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
        self.selectors.update(direct_sibling_selector)
        self.selectors.update(direct_parent_selector)
        self.selectors.update(indirect_parent_selector)
        self.selectors.update(parent_sibling_selector)

        return self.selectors

    def find_parent_locator(self,
                            parent : etree._ElementTree,
                            ele_selector : List[str]) -> List[str]:
        selectors = []

        parent_selectors = self.get_basic_selectors(parent)

        for i in parent_selectors:
            for j in ele_selector:
                selectors.append(i + j)
        
        return selectors
        
    
    def find_sibling_locator(self,
                             element : etree._ElementTree,
                             parent : etree._ElementTree,
                             ele_selector : List[str]) -> List[str]:
        selectors = []

        siblings = self.dom_explorer.get_siblings(parent, element)


        if "preceding" in siblings:
            preceding_locators = self.get_basic_selectors(siblings["preceding"])

            for i in preceding_locators:
                for j in ele_selector:
                    selectors.append(f"{i}/preceding-sibling::{j[2:]}")

        if "following" in siblings:
            following_locators = self.get_basic_selectors(siblings["following"])

            for i in following_locators:
                for j in ele_selector:
                    selectors.append(f"{i}/following-sibling::{j[2:]}")

        return selectors
    
    def get_basic_selectors(self, el : etree._ElementTree) -> List[str]:
        tag = el.tag
        selectors = []

        # ID selector
        for id in (el.attrib.get('id') or "").split():
            selectors.append(f"@id='{id}'")

        # Class selectors
        classes = (el.attrib.get('class') or "").split()

        # Single class
        for c in classes:
            selectors.append(f"contains(@class, '{c}')")

        for r in range(2, 4):
            for j in range(0, (len(classes) - r) + 1):
                selectors.append(f'contains(@class, \'{" ".join(classes[j : j + r])}\')')
        
        # text
        text = el.text

        if text:
            selectors.append(f"contains(text(), '{text[:20]}')")

        # Attribute selectors (common ones)
        for attr in ['name', 'type', 'value', 'placeholder', 'aria-label', 'alt', 'title', 'role']:
            if attr in el.attrib and el.attrib[attr].strip():
                selectors.append(f"@{attr}='{el.attrib[attr]}'")

        combos = []
        for j in range(0, len(classes) - 1):
            combos.append(" and ".join(selectors[j : j + 2]))

        selectors.extend(combos)

        selectors = [f"//{tag}[{i}]" for i in selectors]

        return selectors