# LangChain Course - Main Branch

## Overview

This branch serves as the **foundation** of the LangChain course, demonstrating the basic setup and usage of LangChain for building LLM-powered applications.

## Purpose

Introduce the core concepts of LangChain:

- Setting up LLM providers (OpenAI, Ollama)
- Using `PromptTemplate` for structured prompts
- Creating chains with **LCEL (LangChain Expression Language)**

## Features

### LLM Integration

- **OpenAI**: Uses `ChatOpenAI` with `gpt-4o-mini` model
- **Ollama**: Alternative local LLM support via `ChatOllama` (commented out)

### LCEL Chain

Demonstrates the pipe (`|`) operator to chain prompts and models:

```python
chain = summary_prompt | llm
response = chain.invoke({"information": information})
```

### Text Summarization

The example summarizes biographical information and extracts interesting facts.

## File Structure

```
├── main.py           # Main application entry point
├── pyproject.toml    # Project dependencies
├── .env              # Environment variables (API keys)
└── .gitignore        # Git ignore rules
```

## Key Design Decisions

1. **Environment Variables**: Uses `python-dotenv` for secure API key management
2. **Temperature = 0**: Deterministic outputs for consistent results
3. **LCEL over Legacy Chains**: Uses modern LangChain Expression Language for composability

## Getting Started

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Set up your `.env` file:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Differences from Other Branches

This is the **base branch** that other branches build upon. Other branches extend this foundation with:

- Agents and tools (`search-agent`, `react-search-agent`)
- RAG implementations (`rag-gist`, `document-helper`)
- Callback handlers (`tool-calling-search-agent`, `agent-exec-search-agent`)
