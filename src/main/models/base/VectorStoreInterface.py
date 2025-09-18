from abc import ABC, abstractmethod

class VectorStoreInterface(ABC):

    def __init__(self, docs, model):
        pass

    @abstractmethod
    def from_documents(self, docs, model):
        pass

    @abstractmethod
    def similarity_search_with_score(query, k):
        pass