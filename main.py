import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from utils.logger import setup_logger
from typing import Optional, Union

logger = setup_logger("api.main")

# Initialize FastAPI App
app = FastAPI(
    title="Multi-Agent AI Research System API",
    description="REST API for executing automated AI research tasks.",
    version="1.0.0"
)

# API Models
class ResearchRequest(BaseModel):
    query: str = Field(..., description="The main research topic or question.", json_schema_extra={"example": "Impact of Quantum Computing on Cryptography"})

class TextRequest(BaseModel):
    text: str = Field(..., description="Text payload for summarization or fact-checking.")

class APIResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    data: Union[str, dict, None] = None

# Routes
@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Multi-Agent AI Research System API is running smoothly."}

@app.post("/research", response_model=APIResponse, tags=["Orchestration"])
async def execute_research(request: ResearchRequest):
    """Executes the full 7-agent research pipeline."""
    logger.info(f"API Request received for /research: {request.query}")
    from chains.research_chain import run_research_pipeline

    try:
        final_report = run_research_pipeline(request.query)
        return APIResponse(status="success", message="Research completed successfully.", data=final_report)
    except Exception as e:
        logger.error(f"API Error in /research: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=APIResponse, tags=["Agents"])
async def execute_search(request: ResearchRequest):
    """Executes just the Search Agent (DuckDuckGo, Wiki, Arxiv)."""
    logger.info(f"API Request received for /search: {request.query}")
    from agents.search import SearchAgent

    try:
        search_agent = SearchAgent()
        result = search_agent.run(request.query)
        # Handle both object-like and string returns from the agent
        if hasattr(result, 'model_dump'):
            return APIResponse(status="success", message="Search completed.", data=result.model_dump())
        else:
            return APIResponse(status="success", message="Search completed.", data=str(result))
    except Exception as e:
        logger.error(f"API Error in /search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize", response_model=APIResponse, tags=["Agents"])
async def execute_summarize(request: TextRequest):
    """Executes just the Summarizer Agent on provided text."""
    logger.info("API Request received for /summarize.")
    from agents.summarizer import SummarizerAgent

    try:
        summarizer = SummarizerAgent()
        summary_result = summarizer.run(request.text)
        # Handle both object-like and string returns from the agent
        if hasattr(summary_result, 'summary'):
            return APIResponse(message="Summarization completed.", data=summary_result.summary)
        else:
            return APIResponse(message="Summarization completed.", data=str(summary_result))
    except Exception as e:
        logger.error(f"API Error in /summarize: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/factcheck", response_model=APIResponse, tags=["Agents"])
async def execute_factcheck(request: TextRequest):
    """Executes just the Fact Checker Agent on provided text."""
    logger.info("API Request received for /factcheck.")
    from agents.fact_checker import FactCheckerAgent

    try:
        checker = FactCheckerAgent()
        factcheck_result = checker.run(request.text)
        # Handle both object-like and string returns from the agent
        if hasattr(factcheck_result, 'confidence') and hasattr(factcheck_result, 'summary'):
            return APIResponse(message="Fact check completed.", data={"confidence": factcheck_result.confidence, "report": factcheck_result.summary})
        else:
            return APIResponse(message="Fact check completed.", data={"report": str(factcheck_result)})
    except Exception as e:
        logger.error(f"API Error in /factcheck: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run Server Configuration
if __name__ == "__main__":
    logger.info("Starting FastAPI Uvicorn Server on port 8000...")
    # We specify reload_dirs to avoid watching the virtual environment directory
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Set to True for development; False for production
        reload_dirs=[
            ".", # For root files like main.py, app.py
            "agents", "chains", "models", "tools", "prompts", 
            "memory", "rag", "utils"
        ]
    )