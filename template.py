import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")

# List of all files and directories required for our Multi-Agent AI Research System
list_of_files = [
    # Root files
    ".env.example",
    "requirements.txt",
    "config.py",
    "app.py",
    "main.py",
    
    # Agents package
    "agents/__init__.py",
    "agents/planner.py",
    "agents/search.py",
    "agents/research.py",
    "agents/fact_checker.py",
    "agents/summarizer.py",
    "agents/critic.py",
    "agents/writer.py",
    
    # Tools package
    "tools/__init__.py",
    "tools/search_tool.py",
    "tools/wiki_tool.py",
    "tools/arxiv_tool.py",
    "tools/web_loader.py",
    "tools/pdf_loader.py",
    
    # Prompts package
    "prompts/__init__.py",
    "prompts/planner_prompt.py",
    "prompts/writer_prompt.py",
    "prompts/critic_prompt.py",
    "prompts/search_prompt.py",
    "prompts/research_prompt.py",
    
    # Models package
    "models/__init__.py",
    "models/llm.py",
    "models/schemas.py",
    
    # Memory package
    "memory/__init__.py",
    "memory/memory.py",
    
    # Chains package
    "chains/__init__.py",
    "chains/research_chain.py",
    
    # RAG package
    "rag/__init__.py",
    "rag/loader.py",
    "rag/splitter.py",
    "rag/embedding.py",
    "rag/retriever.py",
    "rag/database.py",
    
    # Utils package
    "utils/__init__.py",
    "utils/logger.py",
    "utils/helpers.py",
    
    # Tests package
    "tests/__init__.py",
    "tests/test_config.py",
]

for filepath_str in list_of_files:
    filepath = Path(filepath_str)

    # Create directory if it doesn't exist
    if filepath.parent != Path("."):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating directory: {filepath.parent} for the file: {filepath.name}")

    # Create file if it doesn't exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")