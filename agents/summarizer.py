from models.llm import get_llm
from models.schemas import AgentOutput
from utils.logger import setup_logger

logger = setup_logger("agents.summarizer")

class SummarizerAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, text: str) -> AgentOutput:
        logger.info("SummarizerAgent generating structured summary.")
        try:
            prompt = f"Provide a concise executive summary and a detailed breakdown of the following text:\n\n{text}"
            response = self.llm.invoke(prompt)
            return AgentOutput(
                task="Summarization",
                status="SUCCESS",
                confidence=0.95,
                sources=[],
                summary=response.content if hasattr(response, 'content') else str(response)
            )
        except Exception as e:
            logger.error(f"Error in SummarizerAgent: {e}")
            return AgentOutput(task="Summarizer", status="FAILED", confidence=0.0, summary=str(e))