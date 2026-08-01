from models.llm import get_llm
from models.schemas import AgentOutput
from utils.logger import setup_logger

logger = setup_logger("agents.research")

class ResearchAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, goal: str, documents: str) -> AgentOutput:
        logger.info(f"ResearchAgent extracting insights for goal: {goal}")
        try:
            prompt = f"Analyze these documents for the research goal '{goal}' and extract key objective facts:\n\n{documents}"
            response = self.llm.invoke(prompt)
            return AgentOutput(
                task=f"Fact extraction for {goal}",
                status="SUCCESS",
                confidence=0.88,
                sources=[],
                summary=response.content if hasattr(response, 'content') else str(response)
            )
        except Exception as e:
            logger.error(f"Error in ResearchAgent: {e}")
            return AgentOutput(task="Research", status="FAILED", confidence=0.0, summary=str(e))