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

### Step 2 (current)
- Runnable Next.js frontend shell
- Dashboard with backend health status indicator
- Upload, library, chat, and compare page skeletons
- Styled component foundation with Tailwind and Framer Motion

## Repository structure

- backend/: FastAPI API and AI pipeline modules
- frontend/: Next.js app shell and initial pages
- docker/: Container configuration (to be added in upcoming steps)

## Next step

Step 3 will connect the upload page to backend ingestion and implement real PDF parsing/chunking pipeline modules.
