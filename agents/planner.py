from langchain_core.output_parsers import PydanticOutputParser
from models.llm import get_llm
from models.schemas import ResearchPlan
from prompts.planner_prompt import PLANNER_PROMPT
from utils.logger import setup_logger

logger = setup_logger("agents.planner")

class PlannerAgent:
    def __init__(self):
        self.llm = get_llm()
        self.parser = PydanticOutputParser(pydantic_object=ResearchPlan)
        self.chain = PLANNER_PROMPT | self.llm

    def run(self, query: str) -> ResearchPlan:
        logger.info(f"PlannerAgent starting execution for query: {query}")
        try:
            formatted_prompt = PLANNER_PROMPT.format_messages(query=query, chat_history=[])
            response = self.llm.invoke(formatted_prompt)
            # For simplicity, if structured parsing is needed, we can use structured LLM bindings or parse response text.
            # Using structured output feature of LangChain:
            structured_llm = self.llm.with_structured_output(ResearchPlan)
            plan = structured_llm.invoke(f"Research Query: {query}")
            logger.info("PlannerAgent successfully created research plan.")
            return plan
        except Exception as e:
            logger.error(f"Error in PlannerAgent: {e}")
            return ResearchPlan(query=query, subtasks=[query], search_queries=[query])