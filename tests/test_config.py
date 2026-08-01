import pytest
from config import settings

def test_settings_initialization():
    """Verify that settings are loaded properly from the configuration module."""
    assert settings is not None
    assert isinstance(settings.LLM_PROVIDER, str)
    assert isinstance(settings.MODEL_NAME, str)
    assert isinstance(settings.TEMPERATURE, float)
    assert isinstance(settings.MAX_TOKENS, int)
    assert settings.TEMPERATURE >= 0.0
    assert settings.MAX_TOKENS > 0

def test_vector_store_settings():
    """Verify vector store settings are configured correctly."""
    assert settings.VECTOR_STORE_TYPE in ["chroma", "faiss"]
    assert isinstance(settings.CHROMA_PERSIST_DIRECTORY, str)
    assert len(settings.CHROMA_PERSIST_DIRECTORY) > 0