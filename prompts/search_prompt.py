from langchain_core.prompts import ChatPromptTemplate

SEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert Information Retrieval Agent. Your task is to analyze subtasks "
     "and determine optimal search strategies across DuckDuckGo, Wikipedia, and Arxiv."),
    ("human", "Subtask: {subtask}\n\nGenerate optimal search keywords and instructions.")
])