from lxml import etree
from typing import Dict
from langchain.schema import Document

from src.main.searchers import SearchHelper, Searcher
from src.main.models.base import EmbeddingModel, GenerativeModel, VectorStoreInterface

class SearchWithEmbeddings(Searcher):

    def __init__(self, embedding_model : EmbeddingModel, model : GenerativeModel, store : VectorStoreInterface, helper : SearchHelper):
        self.helper = helper
        self.elements = None
        self.store = store
        self.embedding_model = embedding_model
        self.model = model
        self.vectorstore = None
        self.chunks = None
        self.mapping = []

    def setup(self, elements : Dict[int, etree._ElementTree]):
        self.elements = elements

        self.chunks = []
        self.mapping = []  # maps chunk index → element index

        for i, el in self.elements.items():
            chunks = self.helper.element_to_chunks(el)

            for ch in chunks:
                if " " not in ch:
                    continue

                self.mapping.append(i)
                self.chunks.append(self.model.invoke(prompt=f"Give a descriptive name for the given tag {ch}. Give short name only"))

        docs = [Document(ch) for ch in self.chunks]

        self.vectorstore = self.store.from_documents(docs, self.embedding_model)

    def search(self, query : str) -> int:

        results = self.vectorstore.similarity_search_with_score(query, k=1)

        doc, score = results[0]

        idx = self.mapping[self.chunks.index(doc.page_content)]
            
        return idx