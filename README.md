# LangChain Course - Tool Calling Search Agent Branch

## Overview

This branch demonstrates **manual tool calling** with custom callback handlers, showing the low-level mechanics of how LangChain agents work.

## Purpose

Understand the internals of agent execution:

- **Manual tool execution loop** instead of high-level abstractions
- **Custom callback handlers** for logging and debugging
- **Tool binding** and message flow with `ToolMessage`

## Features

### Custom Callback Handler

`callbacks.py` implements `AgentCallbackHandler`:

```python
class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"***Prompt to LLM was:***\n{prompts[0]}")

    def on_llm_end(self, response, **kwargs):
        print(f"***LLM Response:***\n{response.generations[0][0].text}")
```

### Manual Tool Execution Loop

Instead of using `AgentExecutor`, this branch implements the loop manually:

1. Send message to LLM
2. Check for `tool_calls` on AI response
3. Execute tools and append `ToolMessage` results
4. Loop until no more tool calls

### Tool Binding

```python
llm_with_tools = llm.bind_tools(tools)
```

### Example Tool

```python
@tool
def get_text_length(text: str) -> int:
    """Return the length of the text by characters."""
    return len(text.strip())
```

## File Structure

```
├── main.py        # Manual agent loop implementation
├── callbacks.py   # Custom callback handler
├── pyproject.toml
└── .env
```

## Key Design Decisions

1. **Manual Loop**: Educational approach to understand agent internals
2. **Callback Logging**: Visibility into LLM prompts and responses
3. **ToolMessage**: Proper tool result handling with `tool_call_id`
4. **Find Tool Helper**: Utility function to locate tools by name

## Agent Flow

```
User Message → LLM → Tool Calls?
                        ↓ Yes
                Execute Tool → ToolMessage → LLM → ...
                        ↓ No
                Final Answer
```

## Differences from Other Branches

| Compared To               | Difference                               |
| ------------------------- | ---------------------------------------- |
| `search-agent`            | Manual loop vs high-level `create_agent` |
| `agent-exec-search-agent` | Manual loop vs `AgentExecutor`           |
| `react-search-agent`      | Tool calling vs ReAct text parsing       |
