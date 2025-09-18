from abc import ABC, abstractmethod

class EmbeddingModel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def embed_documents(self, texts):
        pass

    @abstractmethod
    def embed_query(self, text):
        pass

    @abstractmethod
    def _embed(self, text):
        pass