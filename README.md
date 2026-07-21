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

### Step 5 (current)
- In-memory retrieval over stored chunks
- Grounded chat responses with citations from processed documents
- Fallback response when no relevant context is available

## Repository structure

- backend/: FastAPI API and AI pipeline modules
- frontend/: Next.js app shell and initial pages
- docker/: Container configuration (to be added in upcoming steps)

## Next step

Step 6 will store chunks in Qdrant and add true vector search + reranking.
