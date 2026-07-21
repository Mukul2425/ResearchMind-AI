from __future__ import annotations

from app.rag.reranker import reranker
from app.rag.vector_store import vector_store


class Retriever:
    async def retrieve(self, project_id: str, query: str, limit: int = 5) -> list[dict]:
        candidates = vector_store.search(query=query, limit=limit * 2, document_id=project_id)
        return reranker.rerank(query=query, results=candidates, limit=limit)


retriever = Retriever()
