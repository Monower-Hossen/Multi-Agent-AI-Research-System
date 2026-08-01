from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import setup_logger

logger = setup_logger("rag.splitter")

def split_documents(docs: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    logger.info(f"Splitting {len(docs)} documents into chunks (size={chunk_size}, overlap={chunk_overlap})")
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        split_docs = splitter.split_documents(docs)
        logger.info(f"Created {len(split_docs)} chunks successfully.")
        return split_docs
    except Exception as e:
        logger.error(f"Error splitting documents: {e}")
        return []