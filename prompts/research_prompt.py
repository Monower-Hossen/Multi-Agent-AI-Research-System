from langchain_core.prompts import ChatPromptTemplate

RESEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert Research & Fact-Extraction Agent. "
     "Read the provided raw documents, extract key facts, remove redundancies, "
     "and rank relevance to the research goal."),
    ("human", "Research Goal: {goal}\n\nRetrieved Documents:\n{documents}\n\nExtract key findings.")
])