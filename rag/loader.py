import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader
from utils.logger import setup_logger

logger = setup_logger("rag.loader")

def load_documents(file_path: str = None, url: str = None) -> list:
    logger.info(f"Loading document from source. File: {file_path}, URL: {url}")
    docs = []
    try:
        if file_path and os.path.exists(file_path):
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                docs = loader.load()
            elif file_path.endswith(".txt"):
                loader = TextLoader(file_path)
                docs = loader.load()
        elif url:
            loader = WebBaseLoader(url)
            docs = loader.load()
        return docs
    except Exception as e:
        logger.error(f"Error loading document: {e}")
        return []