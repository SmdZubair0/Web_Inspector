from trio import Path
from lxml import etree
from typing import TypedDict, List, Dict

class LocatorState(TypedDict):
    raw_element : str # element
    raw_element_dom : str # element with its siblings and parent

    dom : Path

    element_idx : int

    element : etree._ElementTree
    element_dom : etree._ElementTree

    name : str
    
    locators : List[Dict[str, List[str]]]