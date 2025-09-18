from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # keys
    huggingface_api_key: str
    groq_api_key : str

    INTERESTING_TAGS: list[str] = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "span", "strong", "em", "small", "blockquote", "code", "a", "button", "input", "textarea", "select", "option", "label", "img", "svg", "video", "audio", "section", "article", "header", "footer", "nav", "main", "ul", "ol", "li", "table", "thead", "tbody", "tr", "th", "td"]

    # HuggingFaceEmbeddingModel
    embedding_model_url: str = "https://api-inference.huggingface.co/models/sentence-transformers/distilbert-base-nli-mean-tokens"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    element_naming_model: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"

settings = Settings()