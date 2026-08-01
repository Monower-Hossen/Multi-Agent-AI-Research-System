from models.llm import get_llm
from models.schemas import AgentOutput
from utils.logger import setup_logger

logger = setup_logger("agents.critic")

class CriticAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, summary: str) -> AgentOutput:
        logger.info("CriticAgent reviewing draft summary.")
        try:
            prompt = f"Critique the following summary. Identify missing points, structural improvements, or clarity issues:\n\n{summary}"
            response = self.llm.invoke(prompt)
            return AgentOutput(
                task="Critical Review",
                status="SUCCESS",
                confidence=0.89,
                sources=[],
                summary=response.content if hasattr(response, 'content') else str(response)
            )
        except Exception as e:
            logger.error(f"Error in CriticAgent: {e}")
            return AgentOutput(task="Critic", status="FAILED", confidence=0.0, summary=str(e))