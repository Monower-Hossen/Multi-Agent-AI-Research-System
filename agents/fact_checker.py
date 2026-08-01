from models.llm import get_llm
from models.schemas import AgentOutput
from utils.logger import setup_logger

logger = setup_logger("agents.fact_checker")

class FactCheckerAgent:
    def __init__(self):
        self.llm = get_llm()

    def run(self, findings: str) -> AgentOutput:
        logger.info("FactCheckerAgent verifying findings and checking confidence.")
        try:
            prompt = f"Review the following research findings for hallucinations, contradictions, or unsupported claims. Rate confidence from 0.0 to 1.0:\n\n{findings}"
            response = self.llm.invoke(prompt)
            return AgentOutput(
                task="Fact Checking & Verification",
                status="SUCCESS",
                confidence=0.90,
                sources=[],
                summary=response.content if hasattr(response, 'content') else str(response)
            )
        except Exception as e:
            logger.error(f"Error in FactCheckerAgent: {e}")
            return AgentOutput(task="Fact Check", status="FAILED", confidence=0.0, summary=str(e))