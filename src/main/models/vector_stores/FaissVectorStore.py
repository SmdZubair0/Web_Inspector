from langchain_community.vectorstores import FAISS

from src.main.models.base import VectorStoreInterface

class FaissVectorStore(VectorStoreInterface):

    def __init__(self, docs=None, embed_model=None):
        self.docs = docs
        self.embed_model = embed_model
        if docs and embed_model:
            self.index = FAISS.from_documents(docs, embed_model)
        else:
            self.index = None

    @classmethod
    def from_documents(cls, docs, embed_model):
        index = FAISS.from_documents(docs, embed_model)
        obj = cls()
        obj.docs = docs
        obj.embed_model = embed_model
        obj.index = index
        return obj
    
    def similarity_search_with_score(self, query, k=5):
        if not self.index:
            raise ValueError("FAISS index not initialized.")
        return self.index.similarity_search_with_score(query, k)
