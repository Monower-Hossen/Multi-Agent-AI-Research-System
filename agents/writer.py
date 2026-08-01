from langchain_core.prompts import ChatPromptTemplate
from models.llm import get_llm
from utils.logger import setup_logger

logger = setup_logger("agents.writer")

class WriterAgent:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical writer and researcher. Compile a comprehensive, highly professional, well-structured Markdown research report based on the provided inputs, analysis, and critique."),
            ("user", "Research Topic: {topic}\n\nCritique and Refinements: {critique}\n\nDraft Content / Research Data: {research_data}")
        ])
        self.chain = self.prompt | self.llm

    def run(self, topic: str, research_data: str, critique: str = "") -> str:
        logger.info(f"WriterAgent compiling final report for topic: '{topic}'")
        try:
            response = self.chain.invoke({
                "topic": topic,
                "research_data": research_data,
                "critique": critique
            })
            content = response.content if hasattr(response, "content") else str(response)
            logger.info("Successfully generated final research report.")
            return content
        except Exception as e:
            logger.error(f"Error in WriterAgent: {e}")
            return f"Error generating final report: {str(e)}"