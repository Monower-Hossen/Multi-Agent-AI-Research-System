import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HUGGINGFACEHUB_API_TOKEN: str = os.getenv("HUGGINGFACEHUB_API_TOKEN", "") # Retained for potential future use
    
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))
    
    VECTOR_STORE_TYPE: str = os.getenv("VECTOR_STORE_TYPE", "chroma")
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()