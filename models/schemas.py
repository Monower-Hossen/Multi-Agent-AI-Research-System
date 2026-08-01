from typing import List, Optional
from pydantic import BaseModel, Field

class ResearchPlan(BaseModel):
    query: str = Field(..., description="The original user research query.")
    subtasks: List[str] = Field(..., description="Breakdown of subtasks required to answer the query.")
    search_queries: List[str] = Field(..., description="Targeted search keywords or phrases for information retrieval.")

class AgentOutput(BaseModel):
    task: str = Field(..., description="The specific task performed by the agent.")
    status: str = Field(..., description="Execution status, e.g., SUCCESS or FAILED.")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0.")
    sources: List[str] = Field(default=[], description="List of URLs or references utilized.")
    summary: str = Field(..., description="Detailed textual findings or output from the agent.")

class ResearchReport(BaseModel):
    title: str = Field(..., description="Title of the research report.")
    executive_summary: str = Field(..., description="High-level summary of findings.")
    main_findings: List[str] = Field(..., description="Bullet points of key research findings.")
    references: List[str] = Field(..., description="Citations and source links.")
    conclusion: str = Field(..., description="Final concluding remarks.")