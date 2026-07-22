# ResearchMind AI

Your AI-powered research companion that reads, understands, compares, and synthesizes research papers.

## Step-by-step build plan

This repository is developed incrementally to keep progress visible on GitHub activity.
Each commit is scoped to one milestone.

### Step 1
- Monorepo scaffold created
- FastAPI backend skeleton
- Core API routes for health, upload, and chat
- Initial RAG service placeholders

### Step 2
- Runnable Next.js frontend shell
- Dashboard with backend health status indicator
- Upload, library, chat, and compare page skeletons
- Styled component foundation with Tailwind and Framer Motion

### Step 3
- Upload page connected to backend /api/documents/upload
- PDF file validation and upload state handling
- Success/error feedback with returned document ID

### Step 4
- Section-aware PDF parsing with heading detection heuristics
- Semantic chunking pipeline with overlap and section metadata
- Ingestion service wired to parse and chunk uploaded documents

### Step 5
- In-memory retrieval over stored chunks
- Grounded chat responses with citations from processed documents
- Fallback response when no relevant context is available

### Step 6
- Qdrant-backed vector storage for chunk embeddings
- Similarity search retrieval with local fallback behavior
- Ingestion pipeline now writes parsed chunks into the vector index

### Step 7
- Retrieval reranking that combines vector similarity and lexical overlap
- Improved top-k ordering for grounded chat answers
- Better ranking metadata for future evaluation work

### Step 8 (current)
- Debug API for inspecting stored documents and chunks
- Search endpoint for viewing retrieval and reranking results
- Visibility into parsed document metadata for pipeline debugging

## Repository structure

- backend/: FastAPI API and AI pipeline modules
- frontend/: Next.js app shell and initial pages
- docker/: Container configuration (to be added in upcoming steps)

## Next step

Step 9 will add a retrieval evaluation harness and local metrics for search quality.
