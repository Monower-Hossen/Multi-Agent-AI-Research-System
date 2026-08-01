from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert AI Research Planner. Your job is to analyze the user's research query, "
     "break it down into logical subtasks, and formulate targeted search queries. "
     "You must output valid JSON matching the requested schema."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "Research Query: {query}\n\nCreate a comprehensive research plan.")
])