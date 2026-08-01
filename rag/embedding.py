from langchain_huggingface import HuggingFaceEmbeddings
from utils.logger import setup_logger

logger = setup_logger("rag.embedding")

def get_embeddings() -> HuggingFaceEmbeddings:
    logger.info("Initializing HuggingFace Sentence Transformer embeddings model.")
    try:
        # Using a lightweight, high-performance free embedding model
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return embeddings
    except Exception as e:
        logger.error(f"Error loading embedding model: {e}")
        raise e