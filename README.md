# LangChain Course - Document Helper Branch

## Overview

This branch implements a **production-ready Document QA Assistant** with a Streamlit web interface, Tavily web crawling for document ingestion, and Pinecone vector storage.

## Purpose

Build a complete document assistant application:

- **Streamlit chat UI** with session management
- **Tavily web crawling** for documentation ingestion
- **Agent-based RAG** with source citations
- **Async batch processing** for vector storage

## Features

### Streamlit Chat Interface (`main.py`)

- Chat-based UI with message history
- Source citation expandable for each response
- Session management with clear chat functionality
- Spinner feedback during processing

### Core RAG Logic (`core.py`)

Agent-based retrieval with tool artifacts:

```python
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve relevant documentation to help answer queries."""
    retrieved_docs = vectorstore.as_retriever().invoke(query, k=4)
    return serialized, retrieved_docs  # Content + artifact
```

### Web Crawling Ingestion (`ingestion.py`)

Async pipeline with Tavily crawling:

```python
tavily_crawl_results = tavily_crawl.invoke({
    "url": "https://python.langchain.com/",
    "extract_depth": "advanced",
    "max_depth": 3,
})
```

### Logging Utility (`logger.py`)

Colored console output for pipeline monitoring.

## File Structure

```
├── main.py           # Streamlit chat UI
├── core.py           # RAG agent logic
├── ingestion.py      # Tavily crawl + Pinecone indexing
├── logger.py         # Colored logging utility
├── notebooks/        # Demo notebooks
├── pyproject.toml
└── .env
```

## Key Design Decisions

1. **Tool Artifacts**: `response_format="content_and_artifact"` returns both text and raw documents
2. **Async Batch Indexing**: Processes documents in parallel batches
3. **SSL Configuration**: Uses certifi for proper SSL handling
4. **RecursiveCharacterTextSplitter**: 4000 chunk size with 200 overlap
5. **Source Tracking**: Documents maintain URL source metadata

## Running the Application

1. Set up environment:

   ```bash
   uv sync
   ```

2. Configure `.env`:

   ```
   OPENAI_API_KEY=your_key
   TAVILY_API_KEY=your_key
   PINECONE_API_KEY=your_key
   PINECONE_INDEX_NAME=your_index
   ```

3. Ingest documentation:

   ```bash
   python ingestion.py
   ```

4. Run Streamlit app:
   ```bash
   streamlit run main.py
   ```

## Differences from Other Branches

| Compared To    | Difference                              |
| -------------- | --------------------------------------- |
| `rag-gist`     | Full Streamlit app vs CLI script        |
| `search-agent` | Document retrieval vs web search        |
| `main`         | Complete application vs basic LLM chain |
