from lxml import etree
from typing import List

class DomExplorer:

    def __init__(self):
        pass

    def find_all_parents(self,
                         element : etree._ElementTree,
                         element_dom : etree._ElementTree) -> List[etree._ElementTree]:
        # Parent selectors
        parents = [element_dom] # since it is already a parent
        
        parents.append(self.find_parent(element, element_dom))
        
        # Reverse so top parent comes first
        parents = parents[::-1]

        return parents


    def find_parent(self,
                    el : etree._ElementTree,
                    root : etree._ElementTree) -> List[etree._ElementTree]:
        
        el_str = etree.tostring(el) 
        for i in root:  # iterate over child
            for j in i:  # recursively search for the element in the child
                if etree.tostring(j) == el_str:   # searching using strings cause both are different objects (created seperately)
                    return i
        return None
    

    def get_siblings(self,
                     parent : etree._ElementTree,
                     element : etree._ElementTree) -> List[etree._ElementTree]:
        
        # since parent will always have atmost one  element before required element as per elmenet_dom
        siblings = {}
        type = "following"
        for i in parent:

            if (etree.tostring(i) != etree.tostring(element)):
                siblings[type] = i
            else:
                type = "preceding"
        return siblings