from agents.planner import PlannerAgent
from agents.search import SearchAgent
from agents.research import ResearchAgent
from agents.fact_checker import FactCheckerAgent
from agents.summarizer import SummarizerAgent
from agents.critic import CriticAgent
from agents.writer import WriterAgent
from utils.logger import setup_logger

logger = setup_logger("chains.research_chain")

def run_research_pipeline(query: str) -> str:
    logger.info(f"Starting Multi-Agent Research Pipeline for query: {query}")
    try:
        # Step 1: Planner
        planner = PlannerAgent()
        plan = planner.run(query)
        # Handle plan output safely (whether it's an object with subtasks or a string/list)
        subtasks_count = len(plan.subtasks) if hasattr(plan, "subtasks") else len(plan) if isinstance(plan, (list, dict)) else 1
        logger.info(f"Step 1 Complete. Subtasks generated: {subtasks_count}")

        # Step 2: Search Agent
        search_agent = SearchAgent()
        search_output = search_agent.run(query)
        logger.info("Step 2 Complete. Search results collected.")
        # Ensure search_output is a string or extracted safely
        search_text = search_output.summary if hasattr(search_output, "summary") else str(search_output)

        # Step 3: Research Agent
        research_agent = ResearchAgent()
        research_output = research_agent.run(query, search_text)
        logger.info("Step 3 Complete. Facts extracted.")
        research_text = research_output.summary if hasattr(research_output, "summary") else str(research_output)

        # Step 4: Fact Checker Agent
        fact_checker = FactCheckerAgent()
        fact_output = fact_checker.run(research_text)
        confidence = fact_output.confidence if hasattr(fact_output, "confidence") else "N/A"
        logger.info(f"Step 4 Complete. Fact check confidence: {confidence}")
        fact_text = fact_output.summary if hasattr(fact_output, "summary") else str(fact_output)

        # Step 5: Summarizer Agent
        summarizer = SummarizerAgent()
        summary_output = summarizer.run(fact_text)
        logger.info("Step 5 Complete. Summary generated.")
        summary_text = summary_output.summary if hasattr(summary_output, "summary") else str(summary_output)

        # Step 6: Critic Agent
        critic = CriticAgent()
        critique_output = critic.run(summary_text)
        logger.info("Step 6 Complete. Critique generated.")
        critique_text = critique_output.summary if hasattr(critique_output, "summary") else str(critique_output)

        # Step 7: Writer Agent
        writer = WriterAgent()
        final_report = writer.run(query, summary_text, critique_text)
        logger.info("Step 7 Complete. Final research report compiled successfully.")

        # Ensure final return is always a clean string
        if hasattr(final_report, "summary"):
            return final_report.summary
        elif isinstance(final_report, str):
            return final_report
        else:
            return str(final_report)

    except Exception as e:
        logger.error(f"Error in research pipeline execution: {e}")
        return f"# Research Execution Failed\n\nError: {str(e)}"