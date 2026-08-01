from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from utils.logger import setup_logger

logger = setup_logger("models.llm")

def get_llm(temperature: float = None, max_tokens: int = None):
    """Factory function to initialize and return the configured LLM provider."""
    temp = temperature if temperature is not None else settings.TEMPERATURE
    tokens = max_tokens if max_tokens is not None else settings.MAX_TOKENS
    provider = settings.LLM_PROVIDER.lower()

    logger.info(f"Initializing LLM provider: {provider} with model: {settings.MODEL_NAME}")

    if provider == "groq":
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in environment variables.")
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=temp,
            max_tokens=tokens
        )
    else:
        # As 'gemini' is removed, we can either default to groq or raise an error for any other provider.
        # For now, we'll be strict.
        raise ValueError(f"Unsupported LLM provider: '{provider}'. Currently, only 'groq' is supported.")