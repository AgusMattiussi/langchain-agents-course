# LangChain Course - Search Agent Branch

## Overview

This branch implements a **structured output search agent** using LangChain's agent framework with Pydantic schemas for type-safe responses.

## Purpose

Demonstrate how to:

- Build agents with web search capabilities
- Use **Pydantic models** to enforce structured outputs
- Integrate **Tavily Search** as a tool
- Create type-safe agent responses

## Features

### Tavily Search Integration

Uses `TavilySearch` from `langchain_tavily` for web search capabilities. The agent can search for real-time information on the web.

### Structured Output with Pydantic

Defines response schemas in `schemas.py`:

```python
class Source(BaseModel):
    url: str  # Source URL

class AgentResponse(BaseModel):
    answer: str       # The agent's answer
    sources: List[Source]  # List of sources used
```

### Agent Creation with Response Format

```python
agent = create_agent(
    model=llm,
    tools=[TavilySearch()],
    response_format=AgentResponse  # Enforces structured output
)
```

## File Structure

```
├── main.py       # Agent implementation
├── schemas.py    # Pydantic response schemas
├── pyproject.toml
└── .env
```

## Key Design Decisions

1. **Pydantic Schemas**: Type-safe responses with automatic validation
2. **TavilySearch Tool**: Reliable web search with API integration
3. **Response Format**: Agent outputs conform to `AgentResponse` schema
4. **Message-based Interface**: Uses `HumanMessage` for agent input

## Getting Started

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Set up `.env`:

   ```
   OPENAI_API_KEY=your_key
   TAVILY_API_KEY=your_tavily_key
   ```

3. Run:
   ```bash
   python main.py
   ```

## Differences from Other Branches

| Compared To                 | Difference                                            |
| --------------------------- | ----------------------------------------------------- |
| `main`                      | Adds agent framework and Tavily search tool           |
| `tool-calling-search-agent` | Uses high-level `create_agent` vs manual tool calling |
| `react-search-agent`        | Uses structured output vs ReAct pattern               |
