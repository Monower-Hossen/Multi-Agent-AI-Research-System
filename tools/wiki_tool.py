import wikipedia
from utils.logger import setup_logger

logger = setup_logger("tools.wiki")

def search_wikipedia(query: str, sentences: int = 3) -> str:
    logger.info(f"Fetching Wikipedia for: {query}")
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        logger.warning(f"Wikipedia disambiguation error: {e}")
        return f"Disambiguation error found. Options: {e.options[:5]}"
    except Exception as e:
        logger.error(f"Error fetching Wikipedia: {e}")
        return "No Wikipedia page found for this query."