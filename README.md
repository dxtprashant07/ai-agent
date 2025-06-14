# Agentic Workflow using LangGraph

An AI agent workflow that processes user queries by splitting them into sub-tasks and executing them using various tools and APIs.

## Features

- Task planning and splitting using PlanAgent
- Task execution with ToolAgent supporting:
  - Weather queries (using OpenWeatherMap API)
  - Math calculations
  - News summaries (using NewsAPI)
- Automatic typo correction and task refinement
- FastAPI web interface for testing

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   OPENWEATHER_API_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   ```

## Usage

### Running Locally
```bash
cd src
python langgraph_workflow.py
```

### Running the API
```bash
cd src
uvicorn app:app --reload
```
Visit http://localhost:8000/docs to test the API

### Example Queries
- "temperature in Singapore, calculate 45*2"
- "weather in London and Paris"
- "summarize the news"

## Project Structure

- `src/`
  - `langgraph_workflow.py`: Main workflow implementation
  - `app.py`: FastAPI web server
  - `agents/`: PlanAgent and ToolAgent implementations
  - `workflow/`: LangGraph workflow components