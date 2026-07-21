from __future__ import annotations

from app.rag.vector_store import vector_store


class Retriever:
    async def retrieve(self, project_id: str, query: str, limit: int = 5) -> list[dict]:
        return vector_store.search(query=query, limit=limit, document_id=project_id)


retriever = Retriever()
