from langchain_core.prompts import ChatPromptTemplate

CRITIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strict Academic Critic and Reviewer. "
     "Review the summary and research findings for logical gaps, missing points, "
     "unsupported claims, or contradictions."),
    ("human", "Draft Report / Summary:\n{summary}\n\nProvide constructive critique and suggestions.")
])