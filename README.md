# LangChain Course - RAG Gist Branch

## Overview

This branch implements **Retrieval-Augmented Generation (RAG)** using Pinecone vector store, demonstrating both traditional and LCEL-based approaches.

## Purpose

Learn RAG fundamentals:

- **Document ingestion** and text splitting
- **Vector store** setup with Pinecone
- **Retrieval chain** implementation
- **LCEL vs Non-LCEL** comparison

## Features

### Document Ingestion (`ingestion.py`)

```python
loader = TextLoader("blog.txt")
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(document)
PineconeVectorStore.from_documents(texts, embeddings, index_name=...)
```

### RAG Chain (`main.py`)

Two implementations are provided for educational comparison:

#### Without LCEL (Manual Approach)

```python
docs = retriever.invoke(query)
context = format_docs(docs)
messages = prompt_template.format_messages(context=context, question=query)
response = llm.invoke(messages)
```

#### With LCEL (Recommended)

```python
chain = (
    RunnablePassthrough.assign(
        context=itemgetter("question") | retriever | format_docs
    )
    | prompt_template
    | llm
    | StrOutputParser()
)
```

### Vector Store Retrieval

```python
vectorstore = PineconeVectorStore(index_name=..., embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

## File Structure

```
├── main.py        # RAG chain (query time)
├── ingestion.py   # Document ingestion pipeline
├── blog.txt       # Sample document for ingestion
├── pyproject.toml
└── .env
```

## Key Design Decisions

1. **Pinecone**: Managed vector database for production-ready retrieval
2. **OpenAI Embeddings**: High-quality text embeddings
3. **CharacterTextSplitter**: Simple chunking for demonstration
4. **k=3 Retrieval**: Returns top 3 most relevant documents
5. **LCEL Comparison**: Educational comparison between approaches

## LCEL Advantages

| Feature       | Non-LCEL | LCEL                  |
| ------------- | -------- | --------------------- |
| Streaming     | Manual   | Built-in `.stream()`  |
| Async         | Manual   | Built-in `.ainvoke()` |
| Composability | Manual   | Pipe operator `\|`    |
| Observability | Limited  | Better tracing        |

## Differences from Other Branches

| Compared To       | Difference                         |
| ----------------- | ---------------------------------- |
| `main`            | Adds RAG pipeline and vector store |
| `document-helper` | Basic RAG vs full Streamlit app    |
| `search-agent`    | Document retrieval vs web search   |
