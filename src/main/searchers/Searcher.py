from lxml import etree
from typing import List, Tuple
from abc import ABC, abstractmethod

from src.main.searchers import SearchHelper
from src.main.models.base import EmbeddingModel, GenerativeModel, VectorStoreInterface

class Searcher(ABC):

    def __init__(self, embedding_model : EmbeddingModel, model : GenerativeModel, store : VectorStoreInterface, helper : SearchHelper):
        pass

    @abstractmethod
    def setup(self, elements : List[Tuple[int, etree._ElementTree]]):
        pass

    @abstractmethod
    def search(self, query : str) -> int:
        pass