# LangChain Course - ReAct Search Agent Branch

## Overview

This branch implements a **ReAct agent** using LangChain's `AgentExecutor` with Pydantic output parsing and structured response format.

## Purpose

Demonstrate production-ready ReAct agents with:

- **AgentExecutor** for managed execution loops
- **Pydantic output parsing** for structured responses
- **Custom ReAct prompt** with format instructions
- **Tavily Search** for web queries

## Features

### ReAct Agent with AgentExecutor

Uses high-level `create_react_agent` factory:

```python
agent = create_react_agent(llm, tools, prompt=react_prompt_with_format_instructions)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### Pydantic Output Parsing

Parses agent output into typed schema:

```python
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
chain = agent_executor | extract_output | parse_output
```

### Custom ReAct Prompt Template

`prompt.py` defines structured ReAct format with format instructions:

```
Thought → Action → Action Input → Observation → ... → Final Answer
```

### Response Schema

`schemas.py` defines typed response:

```python
class AgentResponse(BaseModel):
    answer: str
    sources: List[Source]
```

## File Structure

```
├── main.py        # Agent setup and execution chain
├── prompt.py      # Custom ReAct prompt template
├── schemas.py     # Pydantic response schemas
├── pyproject.toml
└── .env
```

## Key Design Decisions

1. **AgentExecutor**: Handles iteration limits, error handling, and verbose logging
2. **RunnableLambda Chain**: Post-processes output through extract → parse pipeline
3. **Format Instructions**: Auto-generated from Pydantic schema for LLM guidance
4. **Tavily Integration**: Real-time web search capabilities

## Chain Architecture

```
agent_executor → extract_output → parse_output → AgentResponse
```

## Differences from Other Branches

| Compared To                 | Difference                                               |
| --------------------------- | -------------------------------------------------------- |
| `agent-exec-search-agent`   | Uses `create_react_agent` + AgentExecutor vs manual loop |
| `search-agent`              | Adds ReAct pattern and output parsing                    |
| `tool-calling-search-agent` | Text-based ReAct vs function calling                     |
