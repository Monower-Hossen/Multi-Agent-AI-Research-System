from langchain_community.vectorstores import Chroma, FAISS
from rag.embedding import get_embeddings
from config import settings
from utils.logger import setup_logger

logger = setup_logger("rag.database")

def get_vector_store(docs: list = None, collection_name: str = "research_collection"):
    embeddings = get_embeddings()
    store_type = settings.VECTOR_STORE_TYPE.lower()
    logger.info(f"Initializing vector store using type: {store_type}")

    try:
        if store_type == "faiss":
            if docs:
                vector_store = FAISS.from_documents(docs, embeddings)
                return vector_store
            else:
                # Return empty or dummy if no docs provided initially
                raise ValueError("FAISS requires documents to initialize.")
        else: # Default to Chroma
            if docs:
                vector_store = Chroma.from_documents(
                    documents=docs,
                    embedding=embeddings,
                    collection_name=collection_name,
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY
                )
                return vector_store
            else:
                vector_store = Chroma(
                    collection_name=collection_name,
                    embedding_function=embeddings,
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY
                )
                return vector_store
    except Exception as e:
        logger.error(f"Error initializing vector store: {e}")
        raise e