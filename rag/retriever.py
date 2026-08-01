from rag.database import get_vector_store
from utils.logger import setup_logger

logger = setup_logger("rag.retriever")

def get_retriever(vector_store=None, k: int = 4):
    logger.info(f"Configuring retriever with k={k}")
    try:
        if not vector_store:
            vector_store = get_vector_store()
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        return retriever
    except Exception as e:
        logger.error(f"Error setting up retriever: {e}")
        return None