# core/llm.py
import os
from langchain_groq import ChatGroq

def get_llm():
    """
    This function returns the Groq LLM object.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")

    # বর্তমান সচল Groq মডেল (যেমন: llama-3.1-8b-instant বা llama-3.3-70b-versatile) ব্যবহার করুন
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=api_key,
        temperature=0.7
    )
    
    return llm