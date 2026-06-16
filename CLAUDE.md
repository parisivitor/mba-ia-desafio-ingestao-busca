# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Infrastructure
```bash
docker compose up -d          # Start PostgreSQL + pgvector
docker compose down           # Stop services
docker compose logs postgres  # View database logs
```

### Setup
```bash
cp .env.example .env          # Create env config (edit with API keys, DATABASE_URL, etc.)
pip install -r requirements.txt
```

### Running
```bash
python src/ingest.py          # Parse PDF, chunk text, generate embeddings, store in pgvector
python src/chat.py            # Start interactive chat REPL
```

## Architecture

This is a **RAG (Retrieval-Augmented Generation) pipeline** with three stages:

1. **Ingest** (`src/ingest.py`): Load `document.pdf` → chunk text → generate embeddings via OpenAI or Google API → store embeddings and chunks in PostgreSQL/pgvector. The collection name and PDF path are configurable via env vars.

2. **Search** (`src/search.py`): Given a user question, perform vector similarity search against stored embeddings to retrieve relevant chunks, then pass the retrieved context to an LLM along with a strict Portuguese-language prompt. The prompt forbids the LLM from using external knowledge—only the provided context is allowed, with a fixed response if the answer is not found.

3. **Chat** (`src/chat.py`): Interactive REPL that prompts the user for questions and calls `search_prompt()` to retrieve answers, looping until the user exits.

### Infrastructure

**Vector Database**: PostgreSQL 17 + pgvector extension, provided via Docker (`pgvector/pgvector:pg17` image)
- Default database: `rag`
- Default credentials: `postgres/postgres`
- Port: 5432
- The `bootstrap_vector_ext` compose service enables pgvector on first startup

**Embedding Providers**: The setup supports dual embedding provider selection:
- **OpenAI**: `text-embedding-3-small` (env vars: `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`)
- **Google Gemini**: `models/embedding-001` (env vars: `GOOGLE_API_KEY`, `GOOGLE_EMBEDDING_MODEL`)

Selection is automatic based on which API key is set in `.env`.

### Key Environment Variables

| Variable | Purpose | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | Name of pgvector collection to use | `document_chunks` |
| `PDF_PATH` | Path to PDF file to ingest | `document.pdf` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI embeddings) | `sk-...` |
| `OPENAI_EMBEDDING_MODEL` | OpenAI embedding model name | `text-embedding-3-small` |
| `GOOGLE_API_KEY` | Google API key (if using Gemini embeddings) | `AIza...` |
| `GOOGLE_EMBEDDING_MODEL` | Google embedding model name | `models/embedding-001` |

### Key Dependencies

- **LangChain**: Core framework for RAG pipeline (`langchain`, `langchain-core`, `langchain-text-splitters`, `langchain-postgres`, `langchain-openai`, `langchain-google-genai`)
- **pgvector**: PostgreSQL vector extension for semantic search
- **pypdf**: PDF parsing and text extraction
- **SQLAlchemy**: ORM for database access
- **asyncpg/psycopg**: Async and sync PostgreSQL drivers

### Design Notes

- The prompt in `src/search.py` is intentionally strict and enforces context-only answers in Portuguese. This prevents hallucination and ensures the LLM only uses the ingested document as a knowledge base.
- All three Python modules are scaffolds (`pass` stubs) that the student must implement.
- Configuration is env-driven to support different embedding providers and database setups without code changes.
