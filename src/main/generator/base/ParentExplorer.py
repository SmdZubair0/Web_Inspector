from lxml import etree
from typing import List
from abc import ABC, abstractmethod


class ParentExplorer(ABC):

    @abstractmethod
    def find_parent_locator(self,
                            parent : etree._ElementTree,
                            ele_selector : List[str]) -> List[str]:
        pass