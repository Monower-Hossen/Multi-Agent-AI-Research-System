from duckduckgo_search import DDGS
from utils.logger import setup_logger

logger = setup_logger("tools.search")

def search_duckduckgo(query: str, max_results: int = 5) -> list:
    logger.info(f"Searching DuckDuckGo for: {query}")
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
            return results
    except Exception as e:
        logger.error(f"Error in DuckDuckGo search: {e}")
        return []