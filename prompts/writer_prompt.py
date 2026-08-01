from langchain_core.prompts import ChatPromptTemplate

WRITER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert Technical Writer and Research Author. "
     "Compile the researched facts, summaries, and critiques into a professional "
     "Markdown research report featuring an Executive Summary, Main Findings, References, and Future Work."),
    ("human", "Research Topic: {query}\n\nVerified Findings:\n{findings}\n\nCritique Feedback:\n{critique}\n\nWrite the final report.")
])