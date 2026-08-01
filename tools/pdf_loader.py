from langchain_community.document_loaders import PyPDFLoader
from utils.logger import setup_logger

logger = setup_logger("tools.pdf_loader")

def load_pdf(file_path: str) -> list:
    logger.info(f"Loading PDF file: {file_path}")
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return docs
    except Exception as e:
        logger.error(f"Error loading PDF {file_path}: {e}")
        return []