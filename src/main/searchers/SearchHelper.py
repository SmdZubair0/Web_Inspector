import re
from lxml import etree
from typing import Dict, List

from src.main.core.config import settings

class SearchHelper:

    def __init__(self):
        self.INTERESTING_TAGS = settings.INTERESTING_TAGS

    def filter_elements(self, elements : Dict[int, etree._ElementTree]) -> Dict[int, etree._ElementTree]:

        filtered = {}

        for idx, el in elements.items():

            if len(etree.tostring(el)) < 500:
                if el.tag in self.INTERESTING_TAGS:
                    filtered[idx] = el
                
                elif el.text and el.text.strip() and el.tag != 'script':
                    filtered[idx] = el

        return filtered
    
    def split_long_text(self, text : str, max_len : int = 200) -> List[str]:
        if not text:
            return []
        text = text.strip()
        if len(text) <= max_len:
            return [text]
        # split by sentences
        return [t.strip() for t in re.split(r'[.!?]', text) if t.strip()]
    
    def element_to_chunks(self, el : etree._ElementTree, max_len : int = 200) -> List[str]:

        base = f"<{el.tag}"

        attribs = ['class', 'id', 'name', 'value', 'aria-label']

        for i in attribs:
            if i in el.attrib:
                base += f' {i}="{el.attrib[i]}"'

        base += ">"
        
        # chunk text if too long
        if el.text and el.text.strip():
            chunks = self.split_long_text(el.text, max_len)
            return [f"{base} {c}" for c in chunks]
        
        return [base]