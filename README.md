# Multi-Agent-AI-Research-System

A sophisticated, multi-agent system designed to automate the process of AI-driven research. This project leverages a team of specialized AI agents, each with a distinct role, to take a user's research query and produce a comprehensive, well-structured research report.

The system is exposed via a REST API built with FastAPI, allowing for easy integration and interaction.

## ✨ Features

- **7-Agent Research Pipeline**: An end-to-end automated workflow from query to final report.
- **Specialized AI Agents**: Includes agents for searching, summarizing, fact-checking, and writing.
- **Modular Architecture**: Run the full research pipeline or interact with individual agents.
- **Modern Tech Stack**: Built with FastAPI, Pydantic, and LangChain for robust and scalable performance.
- **Developer Friendly**: Hot-reloading server for a smooth development experience.

## 🏛️ Architecture

The core of this system is a collaborative pipeline of AI agents. While the exact flow can be customized, a typical research task involves:

1.  **Search Agent**: Gathers initial information from various sources (e.g., DuckDuckGo, Wikipedia, Arxiv) based on the user's query.
2.  **Summarizer Agent**: Condenses the collected data into a concise summary.
3.  **Critique Agent**: Reviews the initial draft or data for accuracy, completeness, and potential biases.
4.  **Writer Agent**: Compiles the final, polished research report in Markdown format, incorporating the critique and refined data.

Other agents are involved in planning the research and managing the overall workflow.

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Web Server**: Uvicorn
- **AI/LLM Framework**: LangChain
- **Data Validation**: Pydantic

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An API key for your chosen Large Language Model (LLM), configured in a `.env` file (e.g., `OPENAI_API_KEY=...`).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Monower-Hossen/Multi-Agent-AI-Research-System
    cd Multi-Agent-AI-Research-System
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

You can start the API server directly by running the `main.py` file:

```bash
python main.py
```

The server will start on `http://127.0.0.1:8000` with hot-reloading enabled for development.

## 📖 API Usage

Once the server is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### Endpoints

- `GET /`
  - **Description**: Health check to confirm the API is running.

- `POST /research`
  - **Description**: Executes the full 7-agent research pipeline.
  - **Body**: `{ "query": "Your research topic" }`

- `POST /search`
  - **Description**: Executes only the Search Agent.
  - **Body**: `{ "query": "Your search term" }`

- `POST /summarize` | `POST /factcheck`
  - **Description**: Executes the Summarizer or Fact Checker agent on a given piece of text.
  - **Body**: `{ "text": "The text you want to process..." }`