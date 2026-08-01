from models.llm import get_llm
from models.schemas import AgentOutput
from tools.search_tool import search_duckduckgo
from tools.wiki_tool import search_wikipedia
from tools.arxiv_tool import search_arxiv
from utils.logger import setup_logger

logger = setup_logger("agents.search")

class SearchAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, query: str) -> AgentOutput:
        logger.info(f"SearchAgent executing multi-source search for: {query}")
        try:
            web_results = search_duckduckgo(query, max_results=3)
            wiki_results = search_wikipedia(query, sentences=3)
            arxiv_results = search_arxiv(query, max_results=2)

            sources = [r.get("href", "") for r in web_results if "href" in r]
            sources.extend([p.get("pdf_url", "") for p in arxiv_results])

            summary_text = f"Web Results: {web_results}\n\nWikipedia: {wiki_results}\n\nArxiv: {arxiv_results}"
            
            return AgentOutput(
                task=f"Multi-source search for {query}",
                status="SUCCESS",
                confidence=0.92,
                sources=sources,
                summary=summary_text
            )
        except Exception as e:
            logger.error(f"Error in SearchAgent: {e}")
            return AgentOutput(task="Search", status="FAILED", confidence=0.0, summary=str(e))