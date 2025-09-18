from langchain_groq import ChatGroq

from src.main.core.config import settings
from src.main.models.base import GenerativeModel

class ElementNamingModel(GenerativeModel):

    def __init__(self):
        self.model = ChatGroq(
            api_key = settings.groq_api_key,
            model = settings.element_naming_model
        )

    def invoke(self, prompt):
        
        return self.model.invoke(prompt).content.lower()