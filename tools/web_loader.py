import requests
from bs4 import BeautifulSoup
from utils.logger import setup_logger

logger = setup_logger("tools.web_loader")

def scrape_web_page(url: str) -> str:
    logger.info(f"Scraping web page: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=" ")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:5000] # Truncate to avoid context window overflow
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return f"Failed to scrape URL: {e}"